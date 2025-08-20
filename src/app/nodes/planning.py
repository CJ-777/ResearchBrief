from langchain.chat_models import ChatOpenAI
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

Output must be valid JSON with the following fields::
- topic: (string)
- depth: (integer)
- steps: list of objects with keys:
    - objective: (string) objective of the step
    - rationale: (string) rationale behind chosing the step
    - method: (string)

method can be of following type [search, implement, perform].
"""
)


@retry(max_retries=3, delay=2)
def make_plan(topic: str, depth: int) -> ResearchPlan:
    prompt = prompt_template.format_prompt(topic=topic, depth=depth)
    response = llm(prompt.to_messages())
    # Parse and validate output
    plan = parser.parse(response.content)
    return plan
