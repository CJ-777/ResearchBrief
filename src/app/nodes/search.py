from typing import List
from langchain.tools import BaseTool
from serpapi import GoogleSearch
from src.settings import settings


class SearchTool(BaseTool):
    name: str = "search"
    description: str = (
        "Use this tool to fetch relevant URLs for a given query using SerpAPI."
    )

    def _run(self, query: str) -> List[str]:
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": settings.serp_api_key,
                "num": "10",  # number of results to fetch
            }
            search = GoogleSearch(params)
            results = search.get_dict()

            # Extract URLs from structured SERP results
            urls = [
                item["link"]
                for item in results.get("organic_results", [])
                if "link" in item
            ]
            return urls

        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []

    async def _arun(self, query: str) -> List[str]:
        return self._run(query)


# Wrapper function for your graph node
def run_search(topic: str, queries: List[str]) -> List[str]:
    tool = SearchTool()
    urls: List[str] = []
    for q in queries:
        urls.extend(tool.run(f"{topic} {q}"))
    # Remove duplicates
    return list(set(urls))
