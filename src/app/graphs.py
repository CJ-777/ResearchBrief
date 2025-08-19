from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes.context import summarize_context
from .nodes.planning import make_plan
from .nodes.search import run_search
from .nodes.fetch import fetch_docs
from .nodes.summarize import summarize_sources
from .nodes.synthesize import synthesize
from .nodes.postprocess import validate_and_fix
from .store.history import save_brief


# Checkpointing will be added in Step 2


def build_graph():
    g = StateGraph(GraphState)

    def _context(state: GraphState):
        ctx = summarize_context(state.user_id, state.topic) if state.follow_up else None
        return {"context": ctx}

    def _plan(state: GraphState):
        plan = make_plan(state.topic, state.depth)
        queries = [s.objective for s in plan.steps if s.method == "search"]
        return {"plan": plan, "search_queries": queries}

    def _search(state: GraphState):
        urls = run_search(state.topic, state.search_queries)
        return {"urls": urls}

    def _fetch(state: GraphState):
        docs = fetch_docs(state.urls)
        return {"docs": docs}

    def _summarize(state: GraphState):
        sums = summarize_sources(state.docs)
        return {"summaries": sums}

    def _synthesize(state: GraphState):
        brief = synthesize(state.topic, state.depth, state.summaries, state.context)
        return {"brief": brief}

    def _post(state: GraphState):
        fixed = validate_and_fix(state.brief)
        save_brief(state.user_id, fixed)
        return {"brief": fixed}

    g.add_node("context", _context)
    g.add_node("plan", _plan)
    g.add_node("search", _search)
    g.add_node("fetch", _fetch)
    g.add_node("summarize", _summarize)
    g.add_node("synthesize", _synthesize)
    g.add_node("postprocess", _post)

    # Define edges
    g.set_entry_point("context")
    g.add_edge("context", "plan")
    g.add_edge("plan", "search")
    g.add_edge("search", "fetch")
    g.add_edge("fetch", "summarize")
    g.add_edge("summarize", "synthesize")
    g.add_edge("synthesize", "postprocess")
    g.add_edge("postprocess", END)

    return g.compile()
