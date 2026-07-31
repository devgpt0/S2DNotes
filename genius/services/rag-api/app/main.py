from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    field_validator,
)

from app.rag import (
    CorpusError,
    IndexingInProgressError,
    RagService,
    RetrievalBackendUnavailableError,
    Settings,
    UpstashVectorError,
    validate_relative_paths,
)


class StrictRequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class IndexRequest(StrictRequestModel):
    sync_upstash: StrictBool = True


class RetrieveRequest(StrictRequestModel):
    query: StrictStr = Field(min_length=1, max_length=4_000)
    limit: StrictInt = Field(default=5, ge=1, le=20)
    paths: list[StrictStr] | None = Field(default=None, max_length=100)
    backend: Literal["local", "upstash"] = "local"

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query must not be blank")
        return value

    @field_validator("paths")
    @classmethod
    def paths_must_be_relative(cls, value: list[str] | None) -> list[str] | None:
        if value is not None:
            validate_relative_paths(value)
        return value


class Citation(BaseModel):
    path: str
    topic: str
    heading: str
    checksum: str
    snippet: str
    score: float


class RetrieveResponse(BaseModel):
    query: str
    citations: list[Citation]
    mode: Literal["unavailable", "bm25", "hybrid"]
    backend: Literal["local", "upstash"]
    reranked: bool
    indexed: bool


class IndexResponse(BaseModel):
    state: Literal["indexed"]
    document_count: int
    chunk_count: int
    embedding_status: Literal["ready", "unavailable"]
    vector_backend: Literal["disabled", "faiss", "numpy"]
    upstash_synced: bool
    warnings: list[str]


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    index_state: Literal["idle", "indexing", "indexed", "failed"]
    indexed: bool
    document_count: int
    chunk_count: int
    embedding_status: Literal["uninitialized", "ready", "unavailable"]
    reranker_status: Literal["uninitialized", "ready", "unavailable"]
    vector_backend: Literal["disabled", "faiss", "numpy"]
    upstash_enabled: bool
    upstash_synced: bool
    corpus_available: bool
    last_error: str | None
    warnings: list[str]


class TreeNode(BaseModel):
    name: str
    path: str
    children: list[TreeNode]


class TreeResponse(BaseModel):
    files: list[str]
    tree: list[TreeNode]


def get_service(request: Request) -> RagService:
    return request.app.state.rag_service


def build_tree(paths: list[str]) -> list[TreeNode]:
    nodes: dict[str, TreeNode] = {}
    roots: list[TreeNode] = []
    for path in paths:
        parent_nodes = roots
        path_parts = path.split("/")
        for index, name in enumerate(path_parts):
            node_path = "/".join(path_parts[: index + 1])
            node = nodes.get(node_path)
            if node is None:
                node = TreeNode(name=name, path=node_path, children=[])
                nodes[node_path] = node
                parent_nodes.append(node)
            parent_nodes = node.children
    return roots


def create_app(
    settings: Settings | None = None, service: RagService | None = None
) -> FastAPI:
    resolved_settings = settings or Settings.from_environment()
    rag_service = service or RagService(resolved_settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if resolved_settings.auto_index:
            rag_service.start_background_index()
        yield

    application = FastAPI(title="Genius RAG API", version="1.0.0", lifespan=lifespan)
    application.state.rag_service = rag_service

    @application.get("/health", response_model=HealthResponse)
    def health(
        service_instance: Annotated[RagService, Depends(get_service)],
    ) -> HealthResponse:
        service_status = service_instance.status()
        is_degraded = service_status.state == "failed" or (
            service_status.state == "indexed"
            and service_status.embedding_status == "unavailable"
        )
        return HealthResponse(
            status="degraded" if is_degraded else "ok",
            index_state=service_status.state,
            indexed=service_status.state == "indexed",
            document_count=service_status.document_count,
            chunk_count=service_status.chunk_count,
            embedding_status=service_status.embedding_status,
            reranker_status=service_status.reranker_status,
            vector_backend=service_status.vector_backend,
            upstash_enabled=service_status.upstash_enabled,
            upstash_synced=service_status.upstash_synced,
            corpus_available=service_instance.corpus_dir.is_dir(),
            last_error=service_status.last_error,
            warnings=list(service_status.warnings),
        )

    @application.post("/index", response_model=IndexResponse)
    def index_documents(
        service_instance: Annotated[RagService, Depends(get_service)],
        index_request: IndexRequest | None = None,
    ) -> IndexResponse:
        request_value = index_request or IndexRequest()
        try:
            report = service_instance.index(sync_upstash=request_value.sync_upstash)
        except IndexingInProgressError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except (CorpusError, OSError, ValueError) as error:
            raise HTTPException(status_code=503, detail=str(error)) from error
        return IndexResponse(
            state="indexed",
            document_count=report.document_count,
            chunk_count=report.chunk_count,
            embedding_status=report.embedding_status,
            vector_backend=report.vector_backend,
            upstash_synced=report.upstash_synced,
            warnings=list(report.warnings),
        )

    @application.get("/tree", response_model=TreeResponse)
    def tree(
        service_instance: Annotated[RagService, Depends(get_service)],
    ) -> TreeResponse:
        try:
            files = service_instance.document_paths()
        except (CorpusError, OSError) as error:
            raise HTTPException(status_code=503, detail=str(error)) from error
        return TreeResponse(files=files, tree=build_tree(files))

    @application.post("/retrieve", response_model=RetrieveResponse)
    def retrieve(
        retrieve_request: RetrieveRequest,
        service_instance: Annotated[RagService, Depends(get_service)],
    ) -> RetrieveResponse:
        paths = (
            validate_relative_paths(retrieve_request.paths)
            if retrieve_request.paths is not None
            else None
        )
        try:
            result = service_instance.retrieve(
                retrieve_request.query,
                retrieve_request.limit,
                paths,
                retrieve_request.backend,
            )
        except RetrievalBackendUnavailableError as error:
            raise HTTPException(status_code=503, detail=str(error)) from error
        except UpstashVectorError as error:
            raise HTTPException(status_code=503, detail=str(error)) from error
        return RetrieveResponse(
            query=retrieve_request.query,
            citations=[
                Citation(
                    path=hit.chunk.path,
                    topic=hit.chunk.topic,
                    heading=" > ".join(hit.chunk.heading) or "Document",
                    checksum=hit.chunk.checksum,
                    snippet=hit.chunk.text,
                    score=hit.score,
                )
                for hit in result.hits
            ],
            mode=result.mode,
            backend=result.backend,
            reranked=result.reranked,
            indexed=result.indexed,
        )

    return application


app = create_app()
