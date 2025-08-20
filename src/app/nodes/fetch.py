from datetime import datetime
from typing import List
import requests
from bs4 import BeautifulSoup
from src.app.schemas import SourceDoc


def fetch_docs(urls: List[str]) -> List[SourceDoc]:
    """
    Fetch web content from a list of URLs and return structured SourceDoc objects.
    """
    now = datetime.utcnow()
    docs: List[SourceDoc] = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            title = (
                soup.title.string.strip()
                if soup.title
                else url.split("/")[-1].replace("-", " ").title()
            )

            # Extract text content
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            raw_text = " ".join(paragraphs).strip()

            # Ensure minimum content for schema validation
            if len(raw_text) < 40:
                raw_text = f"Content too short at {url}. Fetched minimal text at {now}."

            docs.append(
                SourceDoc(url=url, title=title, fetched_at=now, raw_text=raw_text)
            )

        except Exception as e:
            # Fallback document for failed fetch
            docs.append(
                SourceDoc(
                    url=url,
                    title=f"Error fetching {url}",
                    fetched_at=now,
                    raw_text=f"Failed to fetch {url}: {str(e)}",
                )
            )

    return docs
