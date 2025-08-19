from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import SourceDoc, SourceSummary
from src.settings import settings

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-oss-20b",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=settings.openrouter_api_key,
    temperature=0,
)

# Parser for structured output
parser = PydanticOutputParser(pydantic_object=SourceSummary)

# Prompt template for summarization
prompt_template = ChatPromptTemplate.from_template(
    """You are an expert researcher. Summarize the following source text into a structured summary.

Source URL: {url}
Title: {title}
Text: {text}

Ignore all documents stating error of any kind like 'error 403', dont process them.

Output MUST be valid JSON with the following fields:
- title: (string) use document title
- key_points: (list of strings) list of 5 main points
- evidence_quotes: (list of strings) 2 supporting quotes
- reliability_score: (float) number between 0 and 1
"""
)


def summarize_sources(docs: List[SourceDoc]) -> List[SourceSummary]:
    summaries = []
    valid_docs = [
        doc
        for doc in docs
        if doc.raw_text
        and len(doc.raw_text.strip()) > 40
        and "Failed to fetch" not in doc.raw_text
    ]
    for doc in valid_docs:
        prompt = prompt_template.format_prompt(
            url=doc.url, title=doc.title or doc.url, text=doc.raw_text
        )
        response = llm(prompt.to_messages())
        summary = parser.parse(response.content)
        summaries.append(summary)
    return summaries
