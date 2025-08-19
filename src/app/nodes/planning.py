from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import ResearchPlan
from src.settings import settings

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=settings.openai_api_key
)

# Use Pydantic parser to enforce schema
parser = PydanticOutputParser(pydantic_object=ResearchPlan)

# Prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are a research assistant. Create a structured research plan for the following topic.

Topic: {topic}
Depth: {depth} (1-5)

Output must match the ResearchPlan schema strictly.
"""
)


def make_plan(topic: str, depth: int) -> ResearchPlan:
    prompt = prompt_template.format_prompt(topic=topic, depth=depth)
    response = llm(prompt.to_messages())

    # Parse and validate output
    plan = parser.parse(response.content)
    return plan
