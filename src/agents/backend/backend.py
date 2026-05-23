from src.graphs.states import EngineeringState
import src
import json


def backend_node(state: EngineeringState):
    print("\n--- BACKEND AGENT ---")

    # =====================================================
    # EXTRACT ARCHITECTURE TASKS
    # =====================================================

    architecture_tasks = state["tasks"]

    user_request = state["user_request"]

    # =====================================================
    # EXTRACT ONLY RELEVANT BACKEND DATA
    # =====================================================

    backend_tasks = architecture_tasks.get("backend_tasks", [])

    shared_tasks = architecture_tasks.get("shared_tasks", [])

    api_contracts = architecture_tasks.get("api_contracts", [])

    database_schema = architecture_tasks.get(
        "database_schema",
        []
    )

    folder_structure = architecture_tasks.get(
        "folder_structure",
        ""
    )

    testing_strategy = architecture_tasks.get(
        "testing_strategy",
        ""
    )

    deployment_notes = architecture_tasks.get(
        "deployment_notes",
        ""
    )

    architecture_overview = architecture_tasks.get(
        "architecture_overview",
        ""
    )

    # =====================================================
    # CREATE LLM PROMPT
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": """
You are a Senior Backend Engineer AI Agent.

You are part of an autonomous AI Engineering Team.

Your responsibility is to implement the backend layer
based on the provided architecture and backend engineering tasks.

You must behave like a production-grade backend engineer.

====================================================
YOUR RESPONSIBILITIES
====================================================

1. Build scalable backend architecture
2. Create modular APIs
3. Implement database models
4. Implement authentication and authorization
5. Implement validation logic
6. Handle errors properly
7. Follow clean architecture principles
8. Write production-grade backend code
9. Handle edge cases
10. Optimize performance and scalability

====================================================
BACKEND STACK
====================================================

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Pydantic
- Docker
- Redis (if needed)

====================================================
IMPORTANT RULES
====================================================

- Generate REAL code
- Do not generate pseudo code
- Use modular scalable architecture
- Use async APIs wherever applicable
- Include validation logic
- Include proper exception handling
- Follow REST API standards
- Follow clean code principles
- Include middleware where required
- Include authentication flow
- Include repository/service layers
- Include environment configuration strategy

====================================================
RETURN FORMAT
====================================================

# Backend Architecture

# Folder Structure

# Database Models

# API Contracts Implemented

# Authentication Flow

# Middleware

# Service Layer

# Repository Layer

# API Routes

# Validation Rules

# Error Handling

# Backend Code

# Deployment Notes

# Security Best Practices

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
BACKEND TASKS
====================================================

{json.dumps(backend_tasks, indent=2)}

====================================================
SHARED TASKS
====================================================

{json.dumps(shared_tasks, indent=2)}

====================================================
API CONTRACTS
====================================================

{json.dumps(api_contracts, indent=2)}

====================================================
DATABASE SCHEMA
====================================================

{json.dumps(database_schema, indent=2)}

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

Now implement the backend application.

Requirements:
- Write production-ready backend code
- Build scalable backend architecture
- Implement APIs
- Implement database models
- Add authentication and authorization
- Handle validation and errors properly
- Follow modular backend architecture
- Follow security best practices
"""
        },
    ]

    # =====================================================
    # STREAM RESPONSE
    # =====================================================

    response = ""

    for part in src.client.chat(
        "gpt-oss:120b-cloud",
        messages=messages,
        stream=True
    ):
        content = part["message"]["content"]

        response += content

        print(content, end="", flush=True)

    # =====================================================
    # RETURN STATE UPDATE
    # =====================================================

    return {
        "generated_code": response,

        "active_task": {
            "task_id": "BACKEND-001",

            "task_title": "Backend System Implementation",

            "assigned_agent": "backend_agent",

            "status": "completed",

            "started_at": "",

            "current_step": "Backend implementation completed",

            "progress_percentage": 100,

            "files_being_modified": [
                "app/api",
                "app/models",
                "app/services",
                "app/repositories",
                "app/core",
                "app/middleware",
                "app/db",
                "app/schemas",
                "app/auth"
            ],

            "blockers": [],

            "logs": [
                "Backend architecture generated",
                "Database models implemented",
                "API routes implemented",
                "Authentication flow implemented"
            ]
        },

        "modified_files": [
            "app/api",
            "app/models",
            "app/services",
            "app/repositories",
            "app/core",
            "app/middleware",
            "app/db",
            "app/schemas",
            "app/auth"
        ]
    }