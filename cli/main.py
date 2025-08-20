# CLI implementation for the project
# Command to run: python -m cli.main --user-id <user_id> --topic <topic> --depth <depth> --follow-up (optional)

import argparse
import asyncio
import json
from src.app.graphs import build_graph
from src.app.state import GraphState


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a research brief from a topic."
    )
    parser.add_argument("--topic", type=str, required=True, help="Research topic")
    parser.add_argument("--depth", type=int, default=2, help="Depth of research (1-5)")
    parser.add_argument(
        "--follow-up", action="store_true", help="Flag for follow-up queries"
    )
    parser.add_argument("--user-id", type=str, required=True, help="User identifier")
    return parser.parse_args()


async def main():
    args = parse_args()
    graph = build_graph()
    state = GraphState(
        user_id=args.user_id,
        topic=args.topic,
        depth=args.depth,
        follow_up=args.follow_up,
    )
    result = await graph.ainvoke(state)

    brief = result.get("brief")
    if brief:
        print(json.dumps(brief.model_dump(), indent=2, default=str))
    else:
        print("No brief generated.")


if __name__ == "__main__":
    asyncio.run(main())
