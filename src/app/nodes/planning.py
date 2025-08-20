from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.app.schemas import ResearchPlan
from src.settings import settings
from utils.retries import retry

# Initialize OpenRouter LLM with GPT-OSS-20B
llm = ChatOpenAI(
    model_name="gpt-oss-20b",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=settings.openrouter_api_key,
    temperature=0,
)

# Pydantic parser to enforce schema
parser = PydanticOutputParser(pydantic_object=ResearchPlan)

# Prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are a research assistant. Create a structured research plan for the following topic.

Topic: {topic}
Depth: {depth} (1-5)

Output must be valid JSON with the following fields:
- topic: (string)
- depth: (integer)
- steps: list of objects with keys:
    - objective: (string) objective of the step
    - rationale: (string) rationale behind choosing the step
    - method: (string)

Method can be one of: [search, implement, perform].
"""
)


@retry(max_retries=3, delay=2)
def make_plan(topic: str, depth: int) -> ResearchPlan:
    """
    Generate a structured research plan for a given topic and depth.
    """
    prompt = prompt_template.format_prompt(topic=topic, depth=depth)
    response = llm(prompt.to_messages())
    plan: ResearchPlan = parser.parse(response.content)
    return plan
