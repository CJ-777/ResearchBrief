from typing import List, Optional
from ..schemas import SourceSummary, FinalBrief, ContextSummary


def synthesize(topic: str, depth: int, summaries: List[SourceSummary], ctx: Optional[ContextSummary]) -> FinalBrief:
    thesis = f"Working thesis on {topic}: synthesized from {len(summaries)} sources."
    sections = [
        {"title": "Background", "bullets": [s.key_points[0] for s in summaries]},
        {"title": "Findings", "bullets": [kp for s in summaries for kp in s.key_points[1:]]},
    ]
    refs = [{"url": s.url, "title": s.title or s.url, "used_in_sections": [0, 1]} for s in summaries]
    limits = ["Mock pipeline; no real retrieval yet."]
    return FinalBrief(topic=topic, depth=depth, context_used=ctx, thesis=thesis, sections=sections, limitations=limits, references=refs)