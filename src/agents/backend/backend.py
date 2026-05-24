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


def create_and_init_backend_project(project_name: str, desktop_path: str = None):
    """
    Create a FastAPI backend project with Python virtual environment
    """
    
    if desktop_path is None:
        desktop_path = str(Path.home() / "Desktop")
    
    project_path = os.path.join(desktop_path, project_name)
    
    print(f"\n📁 Creating Python backend project at: {project_path}")
    
    # Create project directory
    os.makedirs(project_path, exist_ok=True)
    
    print(f"🐍 Creating Python virtual environment...")
    
    try:
        # Create virtual environment
        subprocess.run(
            ["python", "-m", "venv", "venv"],
            cwd=project_path,
            check=True
        )
        print("   ✓ Virtual environment created")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error creating virtual environment: {e}")
        return {
            "success": False,
            "error": str(e),
            "project_path": project_path
        }
    
    # Determine python and pip executables based on OS
    import sys
    if sys.platform == "win32":
        python_exe = os.path.join(project_path, "venv", "Scripts", "python.exe")
        pip_exe = os.path.join(project_path, "venv", "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(project_path, "venv", "bin", "python")
        pip_exe = os.path.join(project_path, "venv", "bin", "pip")
    
    print(f"\n📁 Creating project structure...")
    
    # Create folder structure
    folders = [
        "app",
        "app/api",
        "app/api/routes",
        "app/models",
        "app/services",
        "app/repositories",
        "app/core",
        "app/middleware",
        "app/db",
        "app/schemas",
        "app/auth",
        "tests",
        "migrations"
    ]
    
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)
        print(f"   ✓ Created {folder}/")
    
    print(f"\n📥 Installing backend dependencies...")
    
    # Backend dependencies
    dependencies = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "psycopg2-binary",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "alembic",
        "redis",
        "python-dotenv",
        "cors"
    ]
    
    try:
        subprocess.run(
            [pip_exe, "install", "--upgrade", "pip"],
            cwd=project_path,
            check=True,
            timeout=300
        )
        print("   ✓ pip upgraded")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error upgrading pip: {e}")
    
    try:
        subprocess.run(
            [pip_exe, "install"] + dependencies,
            cwd=project_path,
            check=True,
            timeout=600
        )
        print("   ✓ All dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error installing dependencies: {e}")
        return {
            "success": False,
            "error": str(e),
            "project_path": project_path
        }
    
    print(f"\n⚙️  Installing dev dependencies...")
    
    # Dev dependencies
    dev_dependencies = [
        "pytest",
        "pytest-asyncio",
        "httpx",
        "black",
        "flake8",
        "mypy"
    ]
    
    try:
        subprocess.run(
            [pip_exe, "install"] + dev_dependencies,
            cwd=project_path,
            check=True,
            timeout=300
        )
        print("   ✓ Dev dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error installing dev dependencies: {e}")
    
    print(f"\n📝 Creating requirements.txt...")
    
    try:
        subprocess.run(
            [pip_exe, "freeze"],
            cwd=project_path,
            check=True,
            capture_output=True,
            stdout=open(os.path.join(project_path, "requirements.txt"), "w")
        )
        print("   ✓ requirements.txt generated")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error generating requirements.txt: {e}")
    
    print(f"\n🔧 Creating .env file...")
    
    env_content = """# Backend Configuration
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
DEBUG=True
REDIS_URL=redis://localhost:6379
"""
    
    with open(os.path.join(project_path, ".env"), "w") as f:
        f.write(env_content)
    print("   ✓ .env file created")
    
    print(f"\n📝 Creating .gitignore...")
    
    gitignore_content = """venv/
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
.env
.env.local
*.egg-info/
dist/
build/
.DS_Store
.vscode/
.idea/
*.log
"""
    
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    print("   ✓ .gitignore created")
    
    print(f"\n🚀 Initializing Git repository...")
    
    try:
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            check=True,
            capture_output=True
        )
        print("   ✓ Git repository initialized")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error initializing git: {e}")
    
    print(f"\n✅ Backend project setup completed!")
    print(f"📂 Project location: {project_path}")
    print(f"\n💡 Next steps:")
    print(f"   cd {project_path}")
    if sys.platform == "win32":
        print(f"   .\\venv\\Scripts\\activate")
    else:
        print(f"   source venv/bin/activate")
    print(f"   uvicorn app.main:app --reload")
    
    return {
        "success": True,
        "project_path": project_path,
        "message": f"Backend project initialized at {project_path}"
    }


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
    from src.runtime.streaming import (
        update_node_status,
        append_stream_token,
        append_log
    )

    update_node_status("backend", "running")
    append_log("🔵 Backend started code generation")

    response = ""

    for part in src.client.chat(
        "gpt-oss:120b-cloud",
        messages=messages,
        stream=True
    ):
        content = part["message"]["content"]
        response += content
        append_stream_token("backend", content)
        print(content, end="", flush=True)

    update_node_status("backend", "completed")
    append_log("✅ Backend code generation completed")

    # =====================================================
    # RETURN STATE UPDATE
    # =====================================================

    # Create and initialize backend project on Desktop
    project_result = create_and_init_backend_project(
        project_name="backend-app",
        desktop_path=os.path.join(os.path.expanduser("~"), "Desktop")
    )

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
                "Authentication flow implemented",
                f"Project created at: {project_result.get('project_path', 'N/A')}",
                f"Status: {project_result.get('message', project_result.get('error', 'Unknown'))}"
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