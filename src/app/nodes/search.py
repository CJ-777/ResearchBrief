from typing import List
from langchain.tools import BaseTool
from serpapi import GoogleSearch
from src.settings import settings


class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Fetch relevant URLs for a given query using SerpAPI."

    def _run(self, query: str) -> List[str]:
        """
        Perform a search using SerpAPI and return a list of result URLs.
        """
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": settings.serp_api_key,
                "num": 10,  # number of results
            }
            search = GoogleSearch(params)
            results = search.get_dict()

            # Extract URLs from organic results
            urls = [
                item["link"]
                for item in results.get("organic_results", [])
                if "link" in item
            ]
            return urls

        except Exception as e:
            print(f"Error fetching search results for '{query}': {e}")
            return []

    async def _arun(self, query: str) -> List[str]:
        return self._run(query)


def run_search(topic: str, queries: List[str]) -> List[str]:
    """
    Wrapper for SearchTool: combine topic and queries, fetch URLs, and remove duplicates.
    """
    tool = SearchTool()
    urls: List[str] = []

    for q in queries:
        urls.extend(tool.run(f"{topic} {q}"))

    return list(set(urls))
