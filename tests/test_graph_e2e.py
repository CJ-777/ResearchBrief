import pytest
from src.app.graphs import build_graph
from src.app.state import GraphState
from src.app.schemas import (
    ResearchPlan,
    PlanStep,
    SourceDoc,
    SourceSummary,
    ContextSummary,
    FinalBrief,
)


@pytest.fixture
def fake_graph(monkeypatch):
    """Builds the graph with monkeypatched nodes for deterministic testing."""

    # --- Context ---
    monkeypatch.setattr(
        "src.app.nodes.context.summarize_context",
        lambda user_id, topic: ContextSummary(
            user_id=user_id,
            topics=["AI", "ML"],
            recent_findings=["AI models are growing"],
            outstanding_questions=["What are risks?"],
        ),
    )

    # --- Planning ---
    monkeypatch.setattr(
        "src.app.nodes.planning.make_plan",
        lambda topic, depth: ResearchPlan(
            topic=topic,
            depth=depth,
            steps=[
                PlanStep(
                    objective="Search background",
                    rationale="Need info",
                    method="search",
                ),
                PlanStep(
                    objective="Summarize sources",
                    rationale="Condense info",
                    method="perform",
                ),
            ],
        ),
    )

    # --- Search ---
    monkeypatch.setattr(
        "src.app.nodes.search.run_search",
        lambda topic, queries: ["http://example.com/doc1", "http://example.com/doc2"],
    )

    # --- Fetch ---
    monkeypatch.setattr(
        "src.app.nodes.fetch.fetch_docs",
        lambda urls: [
            SourceDoc(url="http://example.com/doc1", title="Doc1", content="Content 1"),
            SourceDoc(url="http://example.com/doc2", title="Doc2", content="Content 2"),
        ],
    )

    # --- Summarize ---
    monkeypatch.setattr(
        "src.app.nodes.summarize.summarize_sources",
        lambda docs: [
            SourceSummary(
                title="Doc 1 Title",
                key_points=["point1", "point2"],
                evidence_quotes=["quote1", "quote2"],
                reliability_score=0.9,
            ),
            SourceSummary(
                title="Doc 2 Title",
                key_points=["pointA", "pointB"],
                evidence_quotes=["quoteA", "quoteB"],
                reliability_score=0.8,
            ),
        ],
    )

    # --- Synthesize ---
    monkeypatch.setattr(
        "src.app.nodes.synthesize.synthesize",
        lambda summaries, plan: FinalBrief(
            topic="AI",
            depth=2,
            context_used=ContextSummary(
                user_id="test_user",
                topics=["AI"],
                recent_findings=["AI models are growing"],
                outstanding_questions=["What are risks?"],
            ),
            thesis="AI is impactful and rapidly evolving.",
            sections=[
                {
                    "title": "Overview",
                    "content": ["AI is impactful", "Lots of research ongoing"],
                }
            ],
            limitations=["Limited data sources", "Mocked pipeline"],
            references=[
                {"title": "Doc1", "url": "http://example.com/doc1"},
                {"title": "Doc2", "url": "http://example.com/doc2"},
            ],
        ),
    )

    # --- Postprocess ---
    monkeypatch.setattr(
        "src.app.nodes.postprocess.validate_and_fix",
        lambda brief: brief,
    )

    # --- Save Brief ---
    monkeypatch.setattr(
        "src.app.store.history.save_brief",
        lambda user_id, brief: True,
    )

    return build_graph()


def test_graph_e2e(fake_graph):
    """End-to-end test of graph with mocked LLMs and tools."""
    initial_state = GraphState(
        user_id="test_user",
        topic="AI",
        depth=2,
        follow_up=True,
    )

    app = fake_graph
    final_state = app.invoke(initial_state)

    # --- Assertions ---
    assert isinstance(final_state.get("context"), ContextSummary)
    assert isinstance(final_state.get("plan"), ResearchPlan)
    assert final_state.get("urls") != []
    assert all(isinstance(d, SourceDoc) for d in final_state.get("docs"))
    assert all(isinstance(s, SourceSummary) for s in final_state.get("summaries"))
    assert isinstance(final_state.get("brief"), FinalBrief)
