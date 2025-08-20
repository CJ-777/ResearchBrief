from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from .schemas import ResearchPlan, SourceDoc, SourceSummary, FinalBrief, ContextSummary


class GraphState(BaseModel):
    user_id: str
    topic: str
    depth: int
    follow_up: bool
    plan: Optional[ResearchPlan] = None
    context: Optional[ContextSummary] = None
    search_queries: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    docs: List[SourceDoc] = Field(default_factory=list)
    summaries: List[SourceSummary] = Field(default_factory=list)
    brief: Optional[FinalBrief] = None
