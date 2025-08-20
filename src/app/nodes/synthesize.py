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

generate a thesis with valid sections and 

Output must be valid JSON with the following fields::
- topic: string
- depth: integer
- context_used: object with keys:
    - user_id: (string) use the same user id used in context
    - topics: (list of strings) A list of distinct topics recently studied
    - recent_findings: (list of strings) The most recent findings or theses (short summaries)
    - outstanding_questions: (list of strings) Outstanding open research questions that remain unresolved
- thesis: (string) thesis based on the summaries
- sections: (list of dicts) sections in the thesis with the following keys:
    - title: (string) title of section
    - content: (string) content of section
- limitations: (list of strings) limitations of the thesis
- references: (list of dicts) with the following keys:
    - title: (string) title of reference used
    - url: (string) url for the reference
    - author: (string) names of authors
"""
)


@retry(max_retries=3, delay=2)
def synthesize(
    topic: str,
    depth: int,
    summaries: List[SourceSummary],
    ctx: Optional[ContextSummary],
) -> FinalBrief:
    # Prepare summaries text
    summaries_text = ""
    for s in summaries:
        summaries_text += f"Title: {s.title}\nKey Points: {s.key_points}\nQuotes: {s.evidence_quotes}\n"

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
