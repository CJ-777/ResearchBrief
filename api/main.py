# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.app.graphs import build_graph
from src.app.state import GraphState
from src.app.schemas import FinalBrief

app = FastAPI(title="Research Brief Generator")

# build the graph once at startup
graph = build_graph()


class BriefRequest(BaseModel):
    topic: str
    depth: int = 2
    follow_up: bool = False
    user_id: str


@app.post("/brief", response_model=FinalBrief)
async def generate_brief(req: BriefRequest):
    try:
        # initialize state
        state = GraphState(
            user_id=req.user_id,
            topic=req.topic,
            depth=req.depth,
            follow_up=req.follow_up,
        )
        # run graph execution
        result = await graph.ainvoke(state)
        return result["brief"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
