from __future__ import annotations

import re

from core.hybrid_search import HybridSearch
from core.openrouter_llm import OpenRouterLLM
from core.query_router import QueryRouter
from core.search_mode import SearchMode
from data.knowledge_base import(
     ARCHITECTURE_DOCS,
    CODE_MAP_DOCS,
    DEBUGGING_DOCS,
    KNOWN_ISSUES_DOCS,
    MAINTENANCE_DOCS,
    PROJECT_OVERVIEW_DOCS,
    RETRIEVAL_NOTES_DOCS,
    SETUP_AND_RUN_DOCS,
    TESTING_DOCS,
    KNOWLEDGE_BASE_INDEX_DOCS,
)
from document_loader.document_manager import DocumentManager
from nlp.keyword_search import KeywordSearch


class AgentV4:
    MODE_BY_INDEX = {
        "1": SearchMode.CHAT,
        "2": SearchMode.KEYWORD,
        "3": SearchMode.SEMANTIC,
        "4": SearchMode.HYBRID,
    }

    MODE_BY_NAME = {
        "chat": SearchMode.CHAT,
        "keyword": SearchMode.KEYWORD,
        "semantic": SearchMode.SEMANTIC,
        "hybrid": SearchMode.HYBRID,
    }
    RETRIEVAL_FILLER_TOKENS = {
        "a",
        "an",
        "can",
        "could",
        "do",
        "for",
        "how",
        "i",
        "is",
        "me",
        "my",
        "please",
        "should",
        "that",
        "the",
        "this",
        "to",
        "what",
    }

    def __init__(self):
        self.router = QueryRouter()
        self.keyword_engine = KeywordSearch()
        self.hybrid_search = HybridSearch()
        self.llm = OpenRouterLLM()
        self.document_manager = DocumentManager()

        self.semantic_engine = None
        self.awaiting_mode_selection = False

        self.documents: list[str] = []
        self.nodes: list[str] = []
        self.documents = [
            PROJECT_OVERVIEW_DOCS,
            ARCHITECTURE_DOCS,
            SETUP_AND_RUN_DOCS,
            TESTING_DOCS,
            DEBUGGING_DOCS,
            KNOWN_ISSUES_DOCS,
            MAINTENANCE_DOCS,
            CODE_MAP_DOCS,
            RETRIEVAL_NOTES_DOCS,
            KNOWLEDGE_BASE_INDEX_DOCS,
        ]
        self._ingest_documents(self.documents)

    def _build_nodes(self, documents: list[str]) -> list[str]:
        nodes: list[str] = []
        for document in documents:
            nodes.extend(self._split_document_into_nodes(document))
        return nodes

    def _ingest_documents(self, documents: list[str]) -> int:
        new_nodes = self._build_nodes(documents)
        for node in new_nodes:
            self.keyword_engine.add_document(node)
            if self.semantic_engine is not None:
                self.semantic_engine.add_document(node)

        self.documents.extend(documents)
        self.nodes.extend(new_nodes)
        return len(new_nodes)

    def _split_document_into_nodes(self, document: str) -> list[str]:
        lines = document.strip().splitlines()
        if not lines:
            return []

        doc_title = ""
        for line in lines:
            if line.startswith("# "):
                doc_title = line[2:].strip()
                break

        sections: list[str] = []
        current: list[str] = []

        for line in lines:
            if line.startswith("## "):
                if current:
                    sections.append("\n".join(current).strip())
                current = [line]
                continue
            if current:
                current.append(line)

        if current:
            sections.append("\n".join(current).strip())

        if not sections:
            return [document.strip()]

        nodes: list[str] = []
        for section in sections:
            if doc_title:
                nodes.append(f"# {doc_title}\n\n{section}".strip())
            else:
                nodes.append(section)
        return nodes

    def _mode_menu(self) -> str:
        current_mode = self.router.get_mode().value
        return (
            "Select mode:\n"
            "1. chat\n"
            "2. keyword\n"
            "3. semantic\n"
            "4. hybrid\n"
            "Use `/mode <number>` or `/mode <name>`.\n"
            f"Current mode: {current_mode}"
        )

    def _parse_mode(self, value: str) -> SearchMode | None:
        token = value.strip().lower()
        if token in self.MODE_BY_INDEX:
            return self.MODE_BY_INDEX[token]
        return self.MODE_BY_NAME.get(token)

    def _ensure_semantic_engine(self) -> tuple[bool, str | None]:
        if self.semantic_engine is not None:
            return True, None

        try:
            from nlp.embedding_search import EmbeddingSearch

            self.semantic_engine = EmbeddingSearch()
            for node in self.nodes:
                self.semantic_engine.add_document(node)
            return True, None
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            return (
                False,
                "Semantic mode is currently unavailable "
                f"({exc}). Staying in keyword mode.",
            )

    def _activate_mode(self, mode: SearchMode) -> str:
        if mode in (SearchMode.SEMANTIC, SearchMode.HYBRID):
            ready, message = self._ensure_semantic_engine()
            if not ready:
                self.router.set_mode(SearchMode.KEYWORD.value)
                return message or "Semantic engine unavailable."

        self.router.set_mode(mode.value)
        return f"Mode changed to {mode.value.upper()}."

    def _extract_relevant_section(self, query: str, document: str) -> str:
        """Return the most relevant markdown section instead of full document dump."""
        lines = document.splitlines()
        sections: list[tuple[str, str]] = []

        current_title = None
        current_lines: list[str] = []

        for line in lines:
            if line.startswith("## "):
                if current_title is not None:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                current_title = line[3:].strip().lower()
                current_lines = [line]
                continue

            if current_title is not None:
                current_lines.append(line)

        if current_title is not None:
            sections.append((current_title, "\n".join(current_lines).strip()))

        if not sections:
            return document.strip()

        query_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        intent_tokens = {
            "start",
            "run",
            "launch",
            "begin",
            "execute",
            "install",
            "setup",
            "mode",
            "test",
            "debug",
        }

        best_section = sections[0][1]
        best_score = float("-inf")

        for title, content in sections:
            title_tokens = set(re.findall(r"[a-z0-9]+", title))
            content_tokens = set(re.findall(r"[a-z0-9]+", content.lower()))

            score = (3 * len(query_tokens & title_tokens)) + len(query_tokens & content_tokens)

            if query_tokens & {"start", "run", "launch", "begin", "execute"} and "run" in title:
                score += 6
            if query_tokens & {"install", "setup"} and ("setup" in title or "prereq" in title):
                score += 5
            if "mode" in query_tokens and "cli commands" in title:
                score += 5
            if "test" in query_tokens and "test" in title:
                score += 5
            if not (query_tokens & intent_tokens):
                score += 0.1 * len(query_tokens & title_tokens)

            if score > best_score:
                best_score = score
                best_section = content

        return best_section.strip()

    def _normalize_query_for_retrieval(self, query: str) -> str:
        tokens = re.findall(r"[a-z0-9]+", query.lower())
        filtered = [tok for tok in tokens if tok not in self.RETRIEVAL_FILLER_TOKENS]
        if not filtered:
            return query
        return " ".join(filtered)

    def _select_best_document(self, query: str, results: list[tuple[str, float]]) -> str:
        if not results:
            return ""

        query_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        top_k = results[:5]
        best_doc = top_k[0][0]
        best_score = float("-inf")

        for doc, base_score in top_k:
            doc_lower = doc.lower()
            score = float(base_score)

            if query_tokens & {"start", "run", "launch", "execute", "install", "setup"}:
                if "## run" in doc_lower:
                    score += 8.0
                if "## setup" in doc_lower or "setup and run docs" in doc_lower:
                    score += 6.0
                if "uv run " in doc_lower:
                    score += 5.0
                if "## test" in doc_lower:
                    score -= 3.0

            if query_tokens & {"test", "pytest", "unit"}:
                if "## test" in doc_lower:
                    score += 6.0

            if query_tokens & {"mode", "command"}:
                if "## cli commands" in doc_lower:
                    score += 4.0

            if query_tokens & {"debug", "troubleshoot", "issue"}:
                if "## fast debugging workflow" in doc_lower or "known issues docs" in doc_lower:
                    score += 4.0

            if score > best_score:
                best_score = score
                best_doc = doc

        return best_doc

    def _generate_retrieval_answer(self, query: str, mode_name: str, context: str) -> str:
        """Use LLM to synthesize retrieval context; fallback to context when unavailable."""
        if not self.llm.is_configured():
            return context

        response = self.llm.generate_with_context(query, context, mode_name)
        if self.llm.is_failure_message(response):
            return context
        return response

    def handle_mode_change(self, query: str) -> str | None:
        user_input = query.strip()
        lowered = user_input.lower()

        # New command format: /mode
        if lowered.startswith("/mode"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 1:
                self.awaiting_mode_selection = True
                return self._mode_menu()

            mode = self._parse_mode(parts[1])
            if mode is None:
                self.awaiting_mode_selection = True
                return (
                    "Invalid mode selection.\n"
                    f"{self._mode_menu()}"
                )

            self.awaiting_mode_selection = False
            return self._activate_mode(mode)

        # Backward-compatible command format: mode keyword
        if lowered.startswith("mode "):
            mode = self._parse_mode(user_input.split(maxsplit=1)[1])
            if mode is None:
                return (
                    "Invalid mode selection.\n"
                    f"{self._mode_menu()}"
                )
            return self._activate_mode(mode)

        # If user requested the list and then enters only number/name.
        if self.awaiting_mode_selection:
            mode = self._parse_mode(user_input)
            if mode is None:
                return (
                    "Please choose 1, 2, 3, 4 or a mode name.\n"
                    f"{self._mode_menu()}"
                )
            self.awaiting_mode_selection = False
            return self._activate_mode(mode)

        return None

    def handle_load_command(self, query: str) -> str | None:
        user_input = query.strip()
        lowered = user_input.lower()
        if lowered != "load" and not lowered.startswith("load "):
            return None

        parts = user_input.split(maxsplit=1)
        if len(parts) == 1:
            return "Usage: load <file-or-directory-path>"

        path = parts[1].strip()
        if not path:
            return "Usage: load <file-or-directory-path>"

        result = self.document_manager.load(path)
        indexed_nodes = 0
        if result.loaded:
            indexed_nodes = self._ingest_documents([doc.content for doc in result.loaded])

        messages: list[str] = []
        if result.loaded:
            messages.append(
                f"Loaded {len(result.loaded)} document(s) and indexed {indexed_nodes} node(s)."
            )
        if result.skipped:
            messages.append(f"Skipped already-loaded document(s): {len(result.skipped)}.")
        if result.errors:
            preview = " | ".join(result.errors[:3])
            messages.append(f"Load error(s): {preview}")

        if not messages:
            return "No documents were loaded."
        return " ".join(messages)

    def run(self, query: str) -> str:
        load_response = self.handle_load_command(query)
        if load_response:
            return load_response

        mode_response = self.handle_mode_change(query)
        if mode_response:
            return mode_response

        mode = self.router.get_mode()

        if mode == SearchMode.KEYWORD:
            retrieval_query = self._normalize_query_for_retrieval(query)
            results = self.keyword_engine.keyword_search(retrieval_query)
            if not results:
                return "No keyword results found."
            best_doc = self._select_best_document(query, results)
            context = self._extract_relevant_section(query, best_doc)
            return self._generate_retrieval_answer(query, "keyword", context)

        if mode == SearchMode.SEMANTIC:
            ready, message = self._ensure_semantic_engine()
            if not ready:
                return message or "Semantic engine unavailable."
            retrieval_query = self._normalize_query_for_retrieval(query)
            results = self.semantic_engine.semantic_search(retrieval_query)
            if not results:
                return "No semantic results found."
            best_doc = self._select_best_document(query, results)
            context = self._extract_relevant_section(query, best_doc)
            return self._generate_retrieval_answer(query, "semantic", context)

        if mode == SearchMode.HYBRID:
            ready, message = self._ensure_semantic_engine()
            if not ready:
                return message or "Hybrid mode unavailable."
            retrieval_query = self._normalize_query_for_retrieval(query)
            results = self.hybrid_search.search(
                retrieval_query,
                self.keyword_engine,
                self.semantic_engine,
            )
            if not results:
                return "No hybrid results found."
            best_doc = self._select_best_document(query, results)
            context = self._extract_relevant_section(query, best_doc)
            return self._generate_retrieval_answer(query, "hybrid", context)

        return self.llm.generate(query)
