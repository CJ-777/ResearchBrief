from typing import List
from langchain_community.utilities import SerpAPIWrapper
from src.settings import settings

# Initialize SerpAPI tool
serp = SerpAPIWrapper(serpapi_api_key=settings.serp_api_key)


def run_search(topic: str, plan_queries: List[str]) -> List[str]:
    """
    Performs web search for each query and returns list of URLs.
    """
    urls: List[str] = []
    for query in plan_queries:
        results = serp.results(query)  # structured dict response
        if "organic_results" in results:
            for item in results["organic_results"]:
                link = item.get("link")
                if link:
                    urls.append(link)
    return urls
