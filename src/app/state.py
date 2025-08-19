from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
from .schemas import ResearchPlan, SourceDoc, SourceSummary, FinalBrief, ContextSummary


class GraphState(BaseModel):
    user_id: str
    topic: str
    depth: int
    follow_up: bool
    plan: Optional[ResearchPlan] = None
    context: Optional[ContextSummary] = None
    search_queries: List[str] = []
    urls: List[str] = []
    docs: List[SourceDoc] = []
    summaries: List[SourceSummary] = []
    brief: Optional[FinalBrief] = None


CHECKPOINT_NSTAG = "research-briefs" # placeholder; real checkpointer in Step 2