from typing import List
from ..schemas import SourceSummary, SourceDoc


def summarize_sources(docs: List[SourceDoc]) -> List[SourceSummary]:
    outs: List[SourceSummary] = []
    for d in docs:
        outs.append(SourceSummary(
            url=d.url,
            title=d.title,
            key_points=[f"Key point from {d.url}", "Mock point B", "Mock point C"],
            evidence_quotes=[d.raw_text[:60], d.raw_text[60:120]],
            reliability_score=0.4,
        ))
    return outs