from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import ContextSummary, FinalBrief
from src.app.store.history import load_user_history
from src.settings import settings
import json
from utils.retries import retry

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-oss-20b",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=settings.openrouter_api_key,
    temperature=0,
)

# Pydantic parser for schema enforcement
parser = PydanticOutputParser(pydantic_object=ContextSummary)

# Prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are a research assistant. Summarize the user’s recent research activity
    into a structured context summary.

User ID: {user_id}
Topic of current query: {topic}

Here is the recent user history (past briefs):
{history}

Output must be valid JSON with the following fields::
- user_id: (string) use the same user id used in context
- topics: (list of strings) A list of distinct topics recently studied
- recent_findings: (list of strings) The most recent findings or theses (short summaries)
- outstanding_questions: (list of strings) Outstanding open research questions that remain unresolved
"""
)


@retry(max_retries=3, delay=2)
def summarize_context(user_id: str, topic: str) -> ContextSummary:
    # Load last 10 briefs
    history: list[FinalBrief] = load_user_history(user_id, limit=10)

    # Format history as readable JSON summaries
    history_text = "\n".join(
        json.dumps(brief.model_dump(), indent=2) for brief in history
    )

    # Build prompt
    prompt = prompt_template.format_prompt(
        user_id=user_id, topic=topic, history=history_text
    )

    # Call LLM
    response = llm(prompt.to_messages())

    # Parse & validate into schema
    summary = parser.parse(response.content)
    return summary
