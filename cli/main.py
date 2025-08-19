# cli/main.py
import argparse
import asyncio
import json
from src.app.graphs import build_graph
from src.app.state import GraphState

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a research brief from a topic.")
    parser.add_argument("--topic", type=str, required=True, help="Research topic")
    parser.add_argument("--depth", type=int, default=2, help="Depth of research (1-5)")
    parser.add_argument("--follow-up", action="store_true", help="Flag for follow-up queries")
    parser.add_argument("--user-id", type=str, required=True, help="User identifier")
    return parser.parse_args()

async def main():
    args = parse_args()

    # Build the graph once
    graph = build_graph()

    # Initialize state
    state = GraphState(
        user_id=args.user_id,
        topic=args.topic,
        depth=args.depth,
        follow_up=args.follow_up
    )

    # Run the graph asynchronously
    result = await graph.ainvoke(state)

    # Print the final brief as pretty JSON
    brief = result.get("brief")
    if brief:
        print(json.dumps(brief.dict(), indent=2, default=str))
    else:
        print("No brief generated.")

if __name__ == "__main__":
    asyncio.run(main())
