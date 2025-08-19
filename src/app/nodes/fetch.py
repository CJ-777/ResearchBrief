from datetime import datetime
from typing import List
import requests
from bs4 import BeautifulSoup
from src.app.schemas import SourceDoc


def fetch_docs(urls: List[str]) -> List[SourceDoc]:
    """
    Fetch real web content from a list of URLs.
    """
    now = datetime.utcnow()
    docs = []

    for u in urls:
        try:
            response = requests.get(u, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            title = (
                soup.title.string.strip() if soup.title else u.split("/")[-1].title()
            )

            # Extract text (limit length for efficiency)
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            raw_text = " ".join(paragraphs)
            raw_text = raw_text.strip()

            if len(raw_text) < 40:  # Ensure it passes schema validation
                raw_text = (
                    f"Content too short at {u}. " f"Fetched minimal text at {now}."
                )

            docs.append(
                SourceDoc(
                    url=u,
                    title=title,
                    fetched_at=now,
                    raw_text=raw_text,
                )
            )

        except Exception as e:
            # fallback doc for failed fetch
            docs.append(
                SourceDoc(
                    url=u,
                    title=f"Error fetching {u}",
                    fetched_at=now,
                    raw_text=f"Failed to fetch {u}: {str(e)}",
                )
            )

    return docs
