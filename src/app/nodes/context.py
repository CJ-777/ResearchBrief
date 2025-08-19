from ..schemas import ContextSummary
from ..store.history import load_user_history


def summarize_context(user_id: str, topic: str) -> ContextSummary:
    h = load_user_history(user_id)
    topics = list({x["topic"] for x in h[-10:]})
    recent = [x.get("thesis", "")[:120] for x in h[-5:]]
    outstanding = [q for x in h[-5:] for q in x.get("open_questions", [])]
    return ContextSummary(user_id=user_id, topics=topics, recent_findings=recent, outstanding_questions=outstanding)