import pytest
from src.app.store.history import init_db, save_brief, load_user_history
from src.app.schemas import FinalBrief, ContextSummary


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Initialize SQLite DB before tests
    init_db()


@pytest.fixture
def sample_brief():
    return FinalBrief(
        topic="AI in Healthcare",
        depth=2,
        context_used=ContextSummary(
            user_id="user123",
            topics=["AI", "Healthcare"],
            recent_findings=["AI can improve diagnostics."],
            outstanding_questions=["How to ensure patient privacy?"],
        ),
        thesis="AI can enhance medical diagnostics accuracy.",
        sections=[
            {"title": "Introduction", "content": ["Overview of AI applications"]}
        ],
        limitations=["Limited dataset size."],
        references=[{"title": "AI Paper", "url": "https://example.com"}],
    )
