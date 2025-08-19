from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import SourceDoc, SourceSummary
from src.settings import settings

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=settings.openai_api_key
)

# Parser for structured output
parser = PydanticOutputParser(pydantic_object=SourceSummary)

# Prompt template for summarization
prompt_template = ChatPromptTemplate.from_template(
    """You are an expert researcher. Summarize the following source text into a structured summary.

Source URL: {url}
Title: {title}
Text: {text}

Output must match the SourceSummary schema strictly.
- key_points: list of 3 main points
- evidence_quotes: 2 supporting quotes
- reliability_score: number between 0 and 1
"""
)


def summarize_sources(docs: List[SourceDoc]) -> List[SourceSummary]:
    summaries = []
    for doc in docs:
        prompt = prompt_template.format_prompt(
            url=doc.url, title=doc.title or doc.url, text=doc.raw_text
        )
        response = llm(prompt.to_messages())
        summary = parser.parse(response.content)
        summaries.append(summary)
    return summaries
