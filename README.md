# Context-Aware Research Brief Generator

## Problem Statement and Objective

The **Context-Aware Research Brief Generator** is a research assistant system designed to generate structured, evidence-linked research briefs in response to user topics. The system supports **follow-up queries** by summarizing prior user interactions and incorporating this context into subsequent outputs. This enables a more personalized and context-aware research experience.

**Objective:**

* Implement a **LangGraph-based workflow** for orchestrating the research brief generation process.
* Integrate **LangChain** for LLM and tool management.
* Enforce **structured outputs** using Pydantic schemas with validation.
* Provide a **REST API** and a **CLI** for users to generate research briefs.

The system ensures that each brief is evidence-based, structured, and reproducible.

---

## Graph Architecture

The workflow is implemented using **LangGraph**, with each node representing a modular processing step. The workflow ensures clear separation of concerns, modularity, and traceable execution.

```
context -> plan -> search -> fetch -> summarize -> synthesize -> postprocess -> END
```

### Node Functions:

* **context:** Summarizes previous user interactions if the query is marked as a follow-up.
* **plan:** Generates a structured research plan with objectives and search queries.
* **search:** Uses SerpAPI to fetch relevant URLs based on the research plan.
* **fetch:** Retrieves content from URLs and converts it into structured `SourceDoc` objects.
* **summarize:** Produces structured summaries (`SourceSummary`) from the fetched documents.
* **synthesize:** Combines summaries and optional context to create the final research brief (`FinalBrief`).
* **postprocess:** Validates and fixes the final brief, applying custom rules and storing it in the database.

**Graph Flow:** START → context → plan → search → fetch → summarize → synthesize → postprocess → END.

This modular graph allows for **retry logic** at each node, ensures **typed state** propagation, and supports **future checkpointing**.

---

## Model and Tool Selection

### LLMs:

* **OpenRouter:** Free and easy to set up. Used for lightweight or development queries.
* **OpenAI GPT-4:** Paid, high-quality models for production-level synthesis and summarization.
* **Usage:** Both providers are used across LLM nodes: context, planning, summarization, and synthesis.

### Other Tools:

* **SerpAPI:** Fetches relevant URLs for queries defined in the research plan.
* **Retries:** Custom decorator (`retries.py`) handles transient LLM or validation failures.

The combination ensures a balance between cost, ease of setup, and output quality.

---

## Schema Definitions and Validation

All outputs use **Pydantic schemas** for structured validation:

* **ResearchPlan:** Represents structured research steps.
* **SourceDoc:** Contains fetched content and metadata.
* **SourceSummary:** Summarizes each source with key points and evidence.
* **ContextSummary:** Captures user context for follow-up queries.
* **FinalBrief:** Comprehensive brief including thesis, sections, limitations, and references.

Validation ensures consistency, reduces LLM hallucinations, and triggers retries if outputs do not conform.

---

## Deployment Instructions

**Platform:** Railway (free tier)

**Rationale:** Easy to use, quick deployment, and minimal configuration.

### Deployment Steps:

1. Import the GitHub repository into Railway.
2. Use the default build module `nixpacks`.
3. Set a custom start command:

   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```
4. Configure environment variables from `.env.example`:

   ```env
   OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
   OPENROUTER_API_KEY=<YOUR_OPENROUTER_API_KEY>
   SERP_API_KEY=<YOUR_SERP_API_KEY>
   LANGSMITH_API_KEY=<YOUR_LANGSMITH_API_KEY>
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=research-briefs
   LANGSMITH_OTEL_ENABLED=true
   PORT=8000
   ```
5. Build the project and generate a public network access link under `Settings -> Networking`.

### Local Setup (Optional):

```bash
python -m venv env
# Activate venv
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
pip install -r requirements.txt
```

No Docker or Makefiles are required due to Railway’s reproducibility.

---

## Usage

### CLI Usage

```bash
python -m cli.main --user-id <user_id> --topic <topic> --depth <depth> [--follow-up]
```

* `--user-id`: Unique user identifier
* `--topic`: Research topic
* `--depth`: Level of detail (1–5)
* `--follow-up`: Optional flag for follow-up queries

### API Usage

* **Endpoint:** `POST /brief`
* **Interactive Docs:** Navigate to `/docs` in FastAPI Swagger UI to send requests directly.
* **Example Request:**

```json
{
  "topic": "string",
  "depth": 2,
  "follow_up": false,
  "user_id": "string"
}
```

---

## Example Requests and Outputs

**Request:**

```json
{
  "topic": "string",
  "depth": 2,
  "follow_up": false,
  "user_id": "string"
}
```

**Response:**

```json
{
  "topic": "string",
  "depth": 1,
  "context_used": {
    "user_id": "string",
    "topics": ["string"],
    "recent_findings": ["string"],
    "outstanding_questions": ["string"]
  },
  "thesis": "string",
  "sections": [{"additionalProp1": {}}],
  "limitations": ["string"],
  "references": [{"additionalProp1": {}}]
}
```

---

## Cost and Latency Benchmarks

* **Average latency:** ≈ 83.5 seconds per request

  * **Most time-consuming nodes:** synthesis and summarization
* **Median tokens used:** 55,742
* **OpenRouter:** Free with limited daily calls
* **OpenAI:** Paid usage as per plan

Monitored via **LangSmith** for accurate tracking.

---

## Limitations and Areas for Improvement

### Current Limitations

* **API Usage Limits:** OpenRouter’s free tier has restricted calls and tokens per day; exceeding limits can cause failures.
* **Latency:** Synthesis and summarization nodes can experience high latency.

### Future Work

* **Checkpointing:** Current retry mechanism does not persist state if the system crashes; implementing checkpointing will improve reliability.
* **Optimizations:** Caching, parallelization, and improved prompts can reduce latency and enhance output quality.
