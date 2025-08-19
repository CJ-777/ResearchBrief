from langchain.tools import BaseTool
from langchain.utilities import SerpAPIWrapper
from typing import List, ClassVar
from src.settings import settings


class SearchTool(BaseTool):
    name: str = "search"
    description: str = (
        "Use this tool to fetch relevant URLs and summaries for a given query."
    )
    serp: ClassVar[SerpAPIWrapper] = SerpAPIWrapper(
        serpapi_api_key=settings.serp_api_key
    )

    def _run(self, query: str) -> List[str]:
        results = self.serp.run(query)
        # SerpAPI returns string; split by lines or parse URLs
        urls = [
            line.strip()
            for line in results.split("\n")
            if line.strip().startswith("http")
        ]
        return urls

    async def _arun(self, query: str) -> List[str]:
        return self._run(query)


# Wrapper function for your graph node
def run_search(topic: str, queries: List[str]) -> List[str]:
    tool = SearchTool()
    urls = []
    for q in queries:
        urls.extend(tool.run(f"{topic} {q}"))
    # Deduplicate
    return list(set(urls))
