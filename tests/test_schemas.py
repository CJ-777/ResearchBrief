import pytest
from pydantic import ValidationError
from src.app.schemas import FinalBrief, ContextSummary


def test_finalbrief_validation():
    ctx = ContextSummary(
        user_id="u1",
        topics=["t1"],
        recent_findings=["f1"],
        outstanding_questions=["q1"],
    )

    # Valid brief
    brief = FinalBrief(
        topic="Sample",
        depth=3,
        context_used=ctx,
        thesis="Thesis text",
        sections=[{"title": "Intro", "content": ["Point1"]}],
        limitations=["None"],
        references=[{"title": "Ref", "url": "https://example.com"}],
    )
    assert brief.depth == 3

    # Invalid brief: no references
    with pytest.raises(ValidationError):
        FinalBrief(
            topic="Sample",
            depth=2,
            context_used=ctx,
            thesis="Thesis",
            sections=[{"title": "Intro", "content": ["Point1"]}],
            limitations=[],
            references=[],
        )
