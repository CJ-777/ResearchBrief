# Exposes the application through FastAPI
# Command to deploy:


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.app.graphs import build_graph
from src.app.state import GraphState
from src.app.schemas import FinalBrief
from fastapi.responses import RedirectResponse

app = FastAPI(title="Research Brief Generator")

# Build the graph once at startup
graph = build_graph()


class BriefRequest(BaseModel):
    topic: str
    depth: int = 2
    follow_up: bool = False
    user_id: str


@app.post("/brief", response_model=FinalBrief)
async def generate_brief(req: BriefRequest):
    """
    Generate a research brief for a given topic and user.
    """
    try:
        state = GraphState(
            user_id=req.user_id,
            topic=req.topic,
            depth=req.depth,
            follow_up=req.follow_up,
        )
        result = await graph.ainvoke(state)
        brief = result.get("brief")
        if not brief:
            raise HTTPException(status_code=404, detail="No brief generated.")
        return brief
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "FastAPI app is live!"}
