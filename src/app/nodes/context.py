from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import ContextSummary, FinalBrief
from src.app.store.history import load_user_history
from src.settings import settings
import json

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=settings.openai_api_key
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

Please extract:
- A list of distinct topics recently studied
- The most recent findings or theses (short summaries)
- Outstanding open research questions that remain unresolved

Output must strictly match the ContextSummary schema.
"""
)


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
