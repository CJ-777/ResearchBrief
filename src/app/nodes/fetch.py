from datetime import datetime
from typing import List
from ..schemas import SourceDoc


def fetch_docs(urls: List[str]) -> List[SourceDoc]:
    now = datetime.utcnow()
    docs = []
    for u in urls:
        docs.append(SourceDoc(
            url=u,
            title=u.split("/")[-1].title(),
            fetched_at=now,
            raw_text=(
                f"This is mock content for {u}. It includes factual-looking text about the topic. "
                f"We will replace this with real fetched content in Step 2. "
                f"The purpose is to validate schemas and the pipeline end-to-end."
            ),
        ))
    return docs