from typing import List


def run_search(topic: str, plan_queries: List[str]) -> List[str]:
# Mock URLs deterministic from topic
    base = topic.strip().lower().replace(" ", "-")
    return [
    f"https://example.org/{base}/overview",
    f"https://example.org/{base}/latest",
    f"https://example.org/{base}/dataset",
    ]