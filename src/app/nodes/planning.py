from ..schemas import ResearchPlan, PlanStep


def make_plan(topic: str, depth: int) -> ResearchPlan:
    steps = [
    PlanStep(objective=f"Clarify scope for: {topic}", rationale="Ensure focus", method="analyze"),
    PlanStep(objective=f"Identify 3 sources on {topic}", rationale="Coverage", method="search"),
    PlanStep(objective="Summarize each source", rationale="Extract facts", method="analyze"),
    PlanStep(objective="Synthesize findings", rationale="Form thesis", method="synthesize"),
    ]
    return ResearchPlan(topic=topic, depth=depth, steps=steps)