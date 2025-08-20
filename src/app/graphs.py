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
from src.settings import settings
import openai
from langsmith import traceable
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)


@traceable
def build_graph():
    g = StateGraph(GraphState)

    @traceable
    def _context(state: GraphState):
        ctx = summarize_context(state.user_id, state.topic) if state.follow_up else None
        state.context = ctx
        return {"context": ctx}

    @traceable
    def _plan(state: GraphState):
        plan = make_plan(state.topic, state.depth)
        queries = [s.objective for s in plan.steps if s.method == "search"]
        state.plan = plan
        state.search_queries = queries
        return {"plan": plan, "search_queries": queries}

    @traceable
    def _search(state: GraphState):
        urls = run_search(state.topic, state.search_queries)
        state.urls = urls
        return {"urls": urls}

    @traceable
    def _fetch(state: GraphState):
        docs = fetch_docs(state.urls)
        state.docs = docs
        return {"docs": docs}

    @traceable
    def _summarize(state: GraphState):
        sums = summarize_sources(state.docs)
        state.summaries = sums
        return {"summaries": sums}

    @traceable
    def _synthesize(state: GraphState):
        brief = synthesize(state.topic, state.depth, state.summaries, state.context)
        state.brief = brief
        return {"brief": brief}

    @traceable
    def _post(state: GraphState):
        fixed = validate_and_fix(state.brief)
        state.brief = fixed
        save_brief(state.user_id, fixed)
        return {"brief": fixed}

    # Add nodes to graph
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
