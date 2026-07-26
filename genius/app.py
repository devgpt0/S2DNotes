from __future__ import annotations

import importlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import requests
import streamlit as st
from google.genai import errors as genai_errors
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web import cli as streamlit_cli

from genius_app import rag as rag_module

if TYPE_CHECKING:
    from genius_app.rag import (
        IndexStats,
        InMemoryVectorStore,
        LocalEmbeddingModel,
        SearchResult,
        Settings,
        UpstashVectorStore,
    )

EXPECTED_RAG_API_VERSION = 4
if getattr(rag_module, "RAG_API_VERSION", None) != EXPECTED_RAG_API_VERSION:
    rag_module = importlib.reload(rag_module)

APP_DIRECTORY = Path(__file__).resolve().parent
CORPUS_DIRECTORY = APP_DIRECTORY.parent / "learnings"
ENV_FILE = APP_DIRECTORY / ".env"
LOCAL_EMBEDDING_CACHE_FILE = APP_DIRECTORY / ".cache" / "bge-m3-embeddings.npz"
CODE_BLOCK_PATTERN = re.compile(
    r"```(?P<language>[\w.+-]*)[ \t]*\n(?P<code>.*?)```",
    re.DOTALL,
)
Backend = Literal["In-memory", "Upstash Vector"]
IndexTarget = Literal["In-memory", "Upstash Vector", "Both"]
AUTO_INDEX_BOTH = "--index-both" in sys.argv[1:]


@dataclass(frozen=True, slots=True)
class DisplayedMessage:
    role: Literal["user", "assistant"]
    content: str
    sources: tuple[SearchResult, ...] = ()


def render_rich_markdown(content: str) -> None:
    position = 0
    for match in CODE_BLOCK_PATTERN.finditer(content):
        markdown = content[position : match.start()]
        if markdown.strip():
            st.markdown(markdown)

        language = match.group("language").lower()
        code = match.group("code").rstrip()
        if language in {"dot", "graphviz"}:
            st.graphviz_chart(code)
            with st.expander("View diagram source"):
                st.code(code, language="dot")
        elif language in {"latex", "math", "tex"}:
            st.latex(code)
        else:
            st.code(code, language=language or "text", wrap_lines=True)
        position = match.end()

    remaining_markdown = content[position:]
    if remaining_markdown.strip():
        st.markdown(remaining_markdown)


def render_sources(sources: tuple[SearchResult, ...]) -> None:
    if not sources:
        return
    with st.expander("Retrieved sources"):
        for result in sources:
            st.markdown(
                f"`{result.chunk.source}` · chunk {result.chunk.index} · score {result.score:.3f}"
            )


def get_messages() -> list[DisplayedMessage]:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state.messages


def get_memory_store() -> InMemoryVectorStore:
    if "memory_store" not in st.session_state or not isinstance(
        st.session_state.memory_store, rag_module.InMemoryVectorStore
    ):
        st.session_state.memory_store = rag_module.InMemoryVectorStore()
    return st.session_state.memory_store


def build_upstash_store(
    settings: Settings,
) -> UpstashVectorStore:
    return rag_module.UpstashVectorStore.from_settings(
        settings,
        rag_module.LOCAL_EMBEDDING_NAMESPACE,
    )


def build_store(
    backend: Backend,
    settings: Settings,
) -> InMemoryVectorStore | UpstashVectorStore:
    if backend == "In-memory":
        return rag_module.InMemoryVectorStore()
    return build_upstash_store(settings)


@st.cache_resource(show_spinner=False, max_entries=1)
def get_local_embedding_model() -> LocalEmbeddingModel:
    return rag_module.LocalEmbeddingModel(APP_DIRECTORY / ".cache" / "bge-m3-model")


@st.cache_resource(show_spinner=False)
def build_startup_indexes(
    upstash_vector_rest_url: str,
    upstash_vector_rest_token: str,
) -> tuple[InMemoryVectorStore, IndexStats, bool]:
    memory_store = rag_module.InMemoryVectorStore()
    upstash_store = rag_module.UpstashVectorStore(
        upstash_vector_rest_url,
        upstash_vector_rest_token,
        rag_module.LOCAL_EMBEDDING_NAMESPACE,
    )
    existing_upstash_vectors = upstash_store.vector_count()
    stats = rag_module.index_corpus(
        CORPUS_DIRECTORY,
        memory_store,
        get_local_embedding_model(),
        mirror_store=upstash_store,
        cache_file=LOCAL_EMBEDDING_CACHE_FILE,
        mirror_existing_count=existing_upstash_vectors,
    )
    return memory_store, stats, existing_upstash_vectors < stats.chunk_count


def auto_index_both(settings: Settings) -> None:
    if not AUTO_INDEX_BOTH or "auto_index_attempted" in st.session_state:
        return
    if not settings.upstash_vector_rest_url:
        raise ValueError("UPSTASH_VECTOR_REST_URL is required with --index-both")
    if not settings.upstash_vector_rest_token:
        raise ValueError("UPSTASH_VECTOR_REST_TOKEN is required with --index-both")

    st.session_state.auto_index_attempted = True
    with st.spinner("Preparing the learning-document indexes..."):
        memory_store, stats, upstash_was_indexed = build_startup_indexes(
            settings.upstash_vector_rest_url,
            settings.upstash_vector_rest_token,
        )
    st.session_state.memory_store = memory_store
    st.session_state.index_stats = stats
    st.session_state.auto_index_complete = True
    if upstash_was_indexed:
        st.success(
            f"Indexed {stats.document_count} documents into {stats.chunk_count} chunks "
            "in memory and Upstash Vector using BGE-M3 embeddings."
        )
    else:
        st.success(
            f"Indexed {stats.document_count} documents into {stats.chunk_count} in-memory chunks. "
            "The existing BGE-M3 Upstash Vector index was reused."
        )


def show_index_controls(
    target: IndexTarget,
    settings: Settings,
) -> None:
    if not st.sidebar.button("Reindex learnings", type="primary", width="stretch"):
        return

    progress_bar = st.sidebar.progress(0.0, text="Starting index")

    def update_progress(current: int, total: int, message: str) -> None:
        progress_bar.progress(current / total, text=message)

    store: InMemoryVectorStore | UpstashVectorStore
    mirror_store: UpstashVectorStore | None = None
    if target == "Both":
        store = rag_module.InMemoryVectorStore()
        mirror_store = build_upstash_store(settings)
    else:
        store = build_store(target, settings)

    stats = rag_module.index_corpus(
        CORPUS_DIRECTORY,
        store,
        get_local_embedding_model(),
        progress=update_progress,
        mirror_store=mirror_store,
        cache_file=LOCAL_EMBEDDING_CACHE_FILE,
    )

    if isinstance(store, rag_module.InMemoryVectorStore):
        st.session_state.memory_store = store
    st.session_state.index_stats = stats
    progress_bar.empty()
    st.sidebar.success(
        f"Reindexed {stats.document_count} documents into {stats.chunk_count} chunks in {target} "
        "using BGE-M3."
    )


def main() -> None:
    st.set_page_config(page_title="Genius", page_icon="🧠", layout="wide")
    st.title("Genius")
    st.caption("Chat with the documents in the learnings folder.")

    try:
        settings = rag_module.Settings.from_environment(ENV_FILE)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    client = rag_module.create_gemini_client(settings.gemini_api_key)
    try:
        auto_index_both(settings)
    except (
        ValueError,
        RuntimeError,
        OSError,
        requests.RequestException,
        genai_errors.APIError,
    ) as error:
        st.error(f"Automatic indexing failed: {error}")

    backend: Backend = st.sidebar.radio(
        "Chat vector store",
        options=("In-memory", "Upstash Vector"),
    )
    index_target: IndexTarget = st.sidebar.selectbox(
        "Reindex target",
        options=("In-memory", "Upstash Vector", "Both"),
    )
    model = st.sidebar.selectbox("Gemini chat model", options=rag_module.CHAT_MODELS)
    top_k = st.sidebar.slider("Retrieved chunks", min_value=2, max_value=10, value=6)
    st.sidebar.caption(f"Chat embeddings: BGE-M3 · {rag_module.EMBEDDING_DIMENSION:,} dimensions")

    try:
        show_index_controls(index_target, settings)
    except (ValueError, OSError, requests.RequestException, genai_errors.APIError) as error:
        st.sidebar.error(f"Indexing failed: {error}")

    messages = get_messages()
    memory_store = get_memory_store()
    for message in messages:
        with st.chat_message(message.role):
            render_rich_markdown(message.content)
            render_sources(message.sources)

    if st.sidebar.button("Clear chat", width="stretch"):
        messages.clear()
        st.rerun()

    upstash_configured = bool(
        settings.upstash_vector_rest_url and settings.upstash_vector_rest_token
    )
    ready = not memory_store.is_empty if backend == "In-memory" else upstash_configured
    if not ready:
        if backend == "In-memory":
            st.info("Index the learnings documents to start chatting.")
        else:
            st.info("Configure the Upstash URL and token, then index the documents.")

    question = st.chat_input("Ask about your learning documents", disabled=not ready)
    if not question:
        return

    user_message = DisplayedMessage(role="user", content=question)
    messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(question)

    try:
        store: InMemoryVectorStore | UpstashVectorStore = (
            memory_store if backend == "In-memory" else build_upstash_store(settings)
        )

        with st.chat_message("assistant"):
            with st.status("Thinking...", expanded=True) as activity_status:
                activity_status.write("Understanding your question")

                def show_activity(message: str) -> None:
                    activity_status.write(message)

                results = rag_module.search_documents(
                    question,
                    store,
                    top_k,
                    get_local_embedding_model(),
                    activity=show_activity,
                )
                activity_status.write("Preparing source-grounded context")
                history = [
                    rag_module.ChatTurn(role=message.role, content=message.content)
                    for message in messages[:-1]
                ]
                activity_status.write(f"Generating the response with {model}")
                answer = rag_module.generate_answer(question, results, history, client, model)
                activity_status.update(
                    label=f"Read {len(results)} chunks - Response ready",
                    state="complete",
                    expanded=False,
                )
            render_rich_markdown(answer)
            source_tuple = tuple(results)
            render_sources(source_tuple)
        messages.append(DisplayedMessage(role="assistant", content=answer, sources=source_tuple))
    except (ValueError, OSError, requests.RequestException, genai_errors.APIError) as error:
        st.error(f"Unable to answer: {error}")


def run_application() -> None:
    if get_script_run_ctx(suppress_warning=True) is not None:
        main()
        return

    application_arguments = [argument for argument in sys.argv[1:] if argument != "--"]
    sys.argv = [
        "streamlit",
        "run",
        str(Path(__file__).resolve()),
        "--",
        *application_arguments,
    ]
    streamlit_cli.main()


if __name__ == "__main__":
    run_application()
