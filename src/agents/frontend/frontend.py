from src.graphs.states import EngineeringState
import src
import json
import os
import subprocess
from pathlib import Path
from src.runtime.streaming import (
    update_node_status,
    append_stream_token,
    append_log
)

def frontend_node(state: EngineeringState):
    print("\n--- FRONTEND AGENT ---")

    # =====================================================
    # EXTRACT ARCHITECTURE TASKS
    # =====================================================

    architecture_tasks = state["tasks"]

    user_request = state["user_request"]

    # =====================================================
    # EXTRACT ONLY RELEVANT FRONTEND DATA
    # =====================================================

    frontend_tasks = architecture_tasks.get("frontend_tasks", [])

    shared_tasks = architecture_tasks.get("shared_tasks", [])

    api_contracts = architecture_tasks.get("api_contracts", [])

    folder_structure = architecture_tasks.get("folder_structure", "")

    testing_strategy = architecture_tasks.get("testing_strategy", "")

    architecture_overview = architecture_tasks.get(
        "architecture_overview",
        ""
    )

    deployment_notes = architecture_tasks.get(
        "deployment_notes",
        ""
    )

    # =====================================================
    # CREATE LLM PROMPT
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": """
You are a Senior Frontend Engineer AI Agent.

You are part of an autonomous AI Engineering Team.

Your responsibility is to implement the frontend layer
based on the provided architecture and frontend engineering tasks.

You must behave like a production-grade frontend engineer.

====================================================
YOUR RESPONSIBILITIES
====================================================

1. Build scalable frontend architecture
2. Create reusable UI components
3. Implement responsive UI
4. Integrate APIs properly
5. Handle loading/error states
6. Follow accessibility standards
7. Follow modular architecture
8. Write production-grade TypeScript code
9. Handle edge cases
10. Optimize performance

====================================================
FRONTEND STACK
====================================================

- React
- TypeScript
- TailwindCSS
- React Query
- Axios
- Zustand or Redux Toolkit
- Feature-based folder structure

====================================================
IMPORTANT RULES
====================================================

- Generate REAL code
- Do not generate pseudo code
- Use industry best practices
- Use modular scalable architecture
- Use reusable components
- Follow clean code principles
- Follow accessibility best practices
- Handle API errors properly
- Handle loading states properly
- Include proper typing
- Include proper folder structure

====================================================
RETURN FORMAT
====================================================

# Folder Structure

# Component Breakdown

# State Management

# API Layer

# Frontend Code

# Edge Cases Handled

# Accessibility Notes

# Performance Optimizations
"""
        },
        {
            "role": "user",
            "content": f"""
USER REQUEST:
{user_request}

====================================================
ARCHITECTURE OVERVIEW
====================================================

{architecture_overview}

====================================================
FRONTEND TASKS
====================================================

{json.dumps(frontend_tasks, indent=2)}

====================================================
SHARED TASKS
====================================================

{json.dumps(shared_tasks, indent=2)}

====================================================
API CONTRACTS
====================================================

{json.dumps(api_contracts, indent=2)}

====================================================
FOLDER STRUCTURE
====================================================

{folder_structure}

====================================================
TESTING STRATEGY
====================================================

{testing_strategy}

====================================================
DEPLOYMENT NOTES
====================================================

{deployment_notes}

====================================================
IMPLEMENTATION REQUIREMENTS
====================================================

Now implement the frontend application.

Requirements:
- Write production-ready frontend code
- Create reusable components
- Use TypeScript
- Integrate APIs properly
- Handle loading/error states
- Follow scalable architecture
- Follow accessibility standards
"""
        },
    ]

    # =====================================================
    # STREAM RESPONSE
    # =====================================================
    # STREAM RESPONSE
    # =====================================================

    update_node_status("frontend", "running")
    append_log("🔵 Frontend started code generation")

    response = ""

    for part in src.client.chat(
        "gpt-oss:120b-cloud",
        messages=messages,
        stream=True
    ):
        content = part["message"]["content"]
        response += content
        append_stream_token("frontend", content)

        # print(content, end="", flush=True)

    update_node_status("frontend", "completed")
    append_log("✅ Frontend code generation completed")

    # =====================================================
    # RETURN STATE UPDATE
    # =====================================================

    return {
        "generated_code": response,

        "active_task": {
            "task_id": "FRONTEND-001",

            "task_title": "Frontend Application Implementation",

            "assigned_agent": "frontend_agent",

            "status": "completed",

            "started_at": "",

            "current_step": "Frontend implementation completed",

            "progress_percentage": 100,

            "files_being_modified": [
                "src/components",
                "src/pages",
                "src/services",
                "src/store",
                "src/hooks"
            ],

            "blockers": [],

            "logs": [
                "Frontend architecture generated",
                "Reusable components created",
                "API integration implemented",
                # f"Project created at: {project_result.get('project_path', 'N/A')}",
                # f"Status: {project_result.get('message', project_result.get('error', 'Unknown'))}"
            ]
        },

        "modified_files": [
            "src/components",
            "src/pages",
            "src/services",
            "src/store",
            "src/hooks"
        ]
    }