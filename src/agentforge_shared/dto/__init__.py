"""Request/response DTOs for AgentForge services."""

from .agent import AgentHealthCheck, AgentHeartbeat, AgentRegistration
from .chat import ChatMessage, ChatRequest, ChatResponse
from .embedding import EmbeddingRequest, EmbeddingResponse
from .execution import (
    ExecutionCancelRequest,
    ExecutionRequest,
    ExecutionResponse,
    ExecutionRetryRequest,
)
from .memory import (
    MemoryItem,
    MemoryQueryRequest,
    MemoryRequest,
    MemoryResponse,
    MemorySearchRequest,
    MemorySearchResult,
)
from .rag import RAGContext, RAGIndexRequest, RAGQueryRequest, RAGQueryResponse
from .search import SearchHit, SearchRequest, SearchResponse
from .streaming import StreamEvent, StreamingChunk, StreamMetadata
from .usage import CostEstimate, TokenUsage, UsageReport
from .workflow import (
    WorkflowRequest,
    WorkflowResponse,
    WorkflowRun,
    WorkflowRunRequest,
    WorkflowStep,
)

__all__ = [
    # agents
    "AgentRegistration",
    "AgentHeartbeat",
    "AgentHealthCheck",
    # chat
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    # embeddings
    "EmbeddingRequest",
    "EmbeddingResponse",
    # execution
    "ExecutionRequest",
    "ExecutionResponse",
    "ExecutionCancelRequest",
    "ExecutionRetryRequest",
    # memory
    "MemoryItem",
    "MemoryRequest",
    "MemoryResponse",
    "MemoryQueryRequest",
    "MemorySearchRequest",
    "MemorySearchResult",
    # rag
    "RAGContext",
    "RAGQueryRequest",
    "RAGQueryResponse",
    "RAGIndexRequest",
    # search
    "SearchRequest",
    "SearchResponse",
    "SearchHit",
    # streaming
    "StreamingChunk",
    "StreamEvent",
    "StreamMetadata",
    # usage / cost
    "TokenUsage",
    "CostEstimate",
    "UsageReport",
    # workflows
    "WorkflowStep",
    "WorkflowRequest",
    "WorkflowResponse",
    "WorkflowRun",
    "WorkflowRunRequest",
]
