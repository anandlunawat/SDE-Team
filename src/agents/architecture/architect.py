from src.graphs.states import EngineeringState
import src
import json
from src.runtime.streaming import (
    update_node_status,
    append_stream_token,
    append_log
)


def architect_node(state: EngineeringState):
    architecture_plan = state["architecture_plan"]
    user_request = state["user_request"]
    
    update_node_status("architect", "running")
    append_log("🔵 Architect started designing architecture")

    messages = [
        {
            "role": "system",
            "content": """
You are a Senior Software Architect AI Agent.

Your responsibility is to convert the provided project plan
into a production-grade technical architecture and executable
engineering task breakdown.

You are working inside an autonomous AI Engineering Team.

The following agents will depend on your output:
- Frontend Agent
- Backend Agent
- Reviewer Agent
- QA Agent

====================================================
IMPORTANT OUTPUT REQUIREMENTS
====================================================

You MUST return STRICTLY VALID JSON.

DO NOT:
- return markdown
- return explanations
- return code fences
- return comments
- return extra text

Return ONLY raw JSON.

====================================================
TASK OBJECT FORMAT
====================================================

Each task inside:
- frontend_tasks
- backend_tasks
- shared_tasks

MUST follow this exact structure:

{
  "id": "TASK-001",
  "title": "Task title",
  "description": "Detailed implementation description",

  "agent": "frontend | backend | shared",

  "priority": "high | medium | low",

  "status": "pending",

  "dependencies": [],

  "files": [],

  "acceptance_criteria": [
    "Criteria 1",
    "Criteria 2"
  ],

  "estimated_complexity": "low | medium | high"
}

====================================================
API CONTRACT FORMAT
====================================================

{
  "endpoint": "/api/v1/auth/login",
  "method": "POST",
  "request": {},
  "response": {}
}

====================================================
DATABASE SCHEMA FORMAT
====================================================

{
  "table": "users",
  "fields": [
    {
      "name": "id",
      "type": "uuid"
    }
  ]
}

====================================================
REQUIRED ROOT JSON STRUCTURE
====================================================

{
  "architecture_overview": "",

  "frontend_tasks": [],

  "backend_tasks": [],

  "shared_tasks": [],

  "api_contracts": [],

  "database_schema": [],

  "folder_structure": "",

  "testing_strategy": "",

  "deployment_notes": ""
}

====================================================
ARCHITECT RESPONSIBILITIES
====================================================

1. Design scalable architecture
2. Create atomic executable tasks
3. Separate frontend/backend responsibilities
4. Define APIs
5. Define DB schema
6. Define auth flow
7. Define folder structure
8. Define testing strategy
9. Define deployment notes
10. Define reusable modules
11. Define integrations

====================================================
RULES
====================================================

- Tasks MUST be executable
- Tasks MUST be implementation-ready
- Prefer modular architecture
- Prefer scalable systems
- Follow production-grade engineering
- Include realistic API contracts
- Include realistic DB schema
- Do not return vague tasks
- Do not skip validation/auth concerns
- Output MUST be parsable JSON
"""
        },
        {
            "role": "user",
            "content": f"""
USER REQUEST:
{user_request}

PLANNING OUTPUT:
{architecture_plan}

Now generate:
1. Technical architecture
2. Engineering task breakdown
3. Frontend/backend separation
4. API contracts
5. Database schema
6. Production-grade implementation tasks

Return STRICT JSON only.
"""
        },
    ]

    response = ""

    for part in src.client.chat(
        "gpt-oss:120b-cloud",
        messages=messages,
        stream=True
    ):
        content = part["message"]["content"]
        response += content
        append_stream_token("architect", content)
        print(content, end="", flush=True)

    # =====================================================
    # SAFE JSON PARSING
    # =====================================================

    try:
        parsed_response = json.loads(response)
        update_node_status("architect", "completed")
        append_log("✅ Architect completed architecture design")
    except Exception as e:
        print("\nJSON PARSE ERROR:", e)
        update_node_status("architect", "error")
        append_log(f"❌ Architect error: JSON parse failed", level="error")

        parsed_response = {
            "architecture_overview": "",
            "frontend_tasks": [],
            "backend_tasks": [],
            "shared_tasks": [],
            "api_contracts": [],
            "database_schema": [],
            "folder_structure": "",
            "testing_strategy": "",
            "deployment_notes": ""
        }

    return {
        "tasks": parsed_response
    }