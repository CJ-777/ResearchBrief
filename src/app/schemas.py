from __future__ import annotations
from pydantic import BaseModel, Field, conint, validator
from typing import List, Optional
from datetime import datetime


class PlanStep(BaseModel):
    objective: str
    rationale: str
    method: str  # expected values: "search", "implement", "perform"


class ResearchPlan(BaseModel):
    topic: str
    depth: conint(ge=1, le=5) = 2
    steps: List[PlanStep]


class SourceDoc(BaseModel):
    url: str
    title: Optional[str] = None
    fetched_at: datetime
    raw_text: str = Field(..., min_length=40)


class SourceSummary(BaseModel):
    title: Optional[str]
    key_points: List[str]
    evidence_quotes: List[str]
    reliability_score: float = Field(..., ge=0, le=1)


class ContextSummary(BaseModel):
    user_id: str
    topics: List[str]
    recent_findings: List[str]
    outstanding_questions: List[str]


class FinalBrief(BaseModel):
    topic: str
    depth: conint(ge=1, le=5)
    context_used: Optional[ContextSummary]
    thesis: str
    sections: List[dict]
    limitations: List[str]
    references: List[dict]

    @validator("references")
    def ensure_references(cls, v):
        if not v:
            raise ValueError("At least one reference is required")
        return v
