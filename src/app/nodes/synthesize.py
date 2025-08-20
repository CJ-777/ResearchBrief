from typing import List, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import SourceSummary, FinalBrief, ContextSummary
from src.settings import settings
from utils.retries import retry

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-oss-20b",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=settings.openrouter_api_key,
    temperature=0,
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

Generate a thesis with valid sections.

Output must be valid JSON with the following fields:
- topic: string
- depth: integer
- context_used: object with keys:
    - user_id: string
    - topics: list of strings
    - recent_findings: list of strings
    - outstanding_questions: list of strings
- thesis: string
- sections: list of dicts with keys:
    - title: string
    - content: string
- limitations: list of strings
- references: list of dicts with keys:
    - title: string
    - url: string
    - author: string
"""
)


@retry(max_retries=3, delay=2)
def synthesize(
    topic: str,
    depth: int,
    summaries: List[SourceSummary],
    ctx: Optional[ContextSummary],
) -> FinalBrief:
    """
    Generate a structured research brief (FinalBrief) from source summaries and optional context.
    """
    # Prepare summaries text
    summaries_text = "\n".join(
        f"Title: {s.title}\nKey Points: {s.key_points}\nQuotes: {s.evidence_quotes}\n"
        for s in summaries
    )

    # Convert context to string
    context_text = str(ctx.dict()) if ctx else "None"

    # Format prompt
    prompt = prompt_template.format_prompt(
        topic=topic, depth=depth, context=context_text, summaries=summaries_text
    )

    # Call LLM
    response = llm(prompt.to_messages())

    # Parse and validate output
    brief: FinalBrief = parser.parse(response.content)
    return brief
