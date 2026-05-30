from typing import TypedDict, List, Dict, Any


# =========================================================
# TASK STRUCTURE
# =========================================================

class EngineeringTask(TypedDict):
    id: str
    title: str
    description: str

    agent: str
    priority: str
    status: str

    dependencies: List[str]

    files: List[str]

    acceptance_criteria: List[str]

    estimated_complexity: str


# =========================================================
# API CONTRACT
# =========================================================

class APIContract(TypedDict):
    endpoint: str
    method: str
    request: Dict[str, Any]
    response: Dict[str, Any]


# =========================================================
# DATABASE SCHEMA
# =========================================================

class DatabaseTable(TypedDict):
    table: str
    fields: List[Dict[str, str]]


# =========================================================
# ARCHITECTURE TASK OUTPUT
# =========================================================

class ArchitectureTasks(TypedDict):

    architecture_overview: str

    frontend_tasks: List[EngineeringTask]

    backend_tasks: List[EngineeringTask]

    shared_tasks: List[EngineeringTask]

    api_contracts: List[APIContract]

    database_schema: List[DatabaseTable]

    folder_structure: str

    testing_strategy: str

    deployment_notes: str


# =========================================================
# ACTIVE TASK STRUCTURE
# =========================================================

class ActiveTask(TypedDict):

    task_id: str

    task_title: str

    assigned_agent: str

    status: str

    started_at: str

    current_step: str

    progress_percentage: int

    files_being_modified: List[str]

    blockers: List[str]

    logs: List[str]


# =========================================================
# COMPLETED TASK STRUCTURE
# =========================================================

class CompletedTask(TypedDict):

    task_id: str

    task_title: str

    completed_by: str

    completion_summary: str

    generated_files: List[str]

    tests_passed: bool

    review_approved: bool

    completion_timestamp: str

    execution_logs: List[str]


# =========================================================
# MAIN STATE
# =========================================================

class EngineeringState(TypedDict):

    # Original user request
    user_request: str

    # Architecture output
    architecture_plan: str

    architecture_approval: str

    # Task Management
    tasks: ArchitectureTasks

    active_task: ActiveTask

    completed_tasks: List[CompletedTask]

    # Generated outputs
    generated_code: str

    # Review system
    review_feedback: str
    review_approved: bool

    # Testing
    test_results: str
    test_passed: bool

    # Debugging
    errors: List[str]
    debug_attempts: int

    # Filesystem
    modified_files: List[str]

    # Memory / Context
    project_context: str