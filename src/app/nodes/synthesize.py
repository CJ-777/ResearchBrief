from typing import List, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import SourceSummary, FinalBrief, ContextSummary
from src.settings import settings

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=settings.openai_api_key
)

# Pydantic parser for structured FinalBrief output
parser = PydanticOutputParser(pydantic_object=FinalBrief)

# Prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are an expert research assistant. Synthesize the following information into a structured research brief.

Topic: {topic}
Depth: {depth}
Context: {context}

Summaries:
{summaries}

Requirements:
- Include thesis, sections (with bullets), limitations, references.
- Output must strictly match the FinalBrief schema.
"""
)


def synthesize(
    topic: str,
    depth: int,
    summaries: List[SourceSummary],
    ctx: Optional[ContextSummary],
) -> FinalBrief:
    # Prepare summaries text
    summaries_text = ""
    for s in summaries:
        summaries_text += f"\nURL: {s.url}\nTitle: {s.title}\nKey Points: {s.key_points}\nQuotes: {s.evidence_quotes}\n"

    context_text = str(ctx.dict()) if ctx else "None"

    # Format prompt
    prompt = prompt_template.format_prompt(
        topic=topic, depth=depth, context=context_text, summaries=summaries_text
    )

    # Call LLM
    response = llm(prompt.to_messages())

    # Parse and validate output
    brief = parser.parse(response.content)
    return brief
