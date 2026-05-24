def architecture_to_markdown(data: dict) -> str:
    md = []

    # =====================================================
    # OVERVIEW
    # =====================================================

    md.append("# 🏗️ Architecture Overview\n")
    md.append(data.get("architecture_overview", "N/A"))

    # =====================================================
    # FRONTEND TASKS
    # =====================================================

    md.append("\n\n# 🎨 Frontend Tasks\n")

    for task in data.get("frontend_tasks", []):
        md.append(f"## {task['id']} — {task['title']}")
        md.append(f"**Priority:** {task['priority']}")
        md.append(f"**Complexity:** {task['estimated_complexity']}")
        md.append(f"**Description:** {task['description']}")

        md.append("\n### Acceptance Criteria")
        for item in task.get("acceptance_criteria", []):
            md.append(f"- {item}")

        md.append("\n### Files")
        for file in task.get("files", []):
            md.append(f"- `{file}`")

        md.append("\n---\n")

    # =====================================================
    # BACKEND TASKS
    # =====================================================

    md.append("\n# ⚙️ Backend Tasks\n")

    for task in data.get("backend_tasks", []):
        md.append(f"## {task['id']} — {task['title']}")
        md.append(f"**Priority:** {task['priority']}")
        md.append(f"**Complexity:** {task['estimated_complexity']}")
        md.append(f"**Description:** {task['description']}")

        md.append("\n### Acceptance Criteria")
        for item in task.get("acceptance_criteria", []):
            md.append(f"- {item}")

        md.append("\n---\n")

    # =====================================================
    # API CONTRACTS
    # =====================================================

    md.append("\n# 🔌 API Contracts\n")

    for api in data.get("api_contracts", []):
        md.append(
            f"## `{api['method']}` {api['endpoint']}"
        )

        md.append("\n### Request")
        md.append(f"```json\n{api['request']}\n```")

        md.append("\n### Response")
        md.append(f"```json\n{api['response']}\n```")

    # =====================================================
    # DATABASE
    # =====================================================

    md.append("\n# 🗄️ Database Schema\n")

    for table in data.get("database_schema", []):
        md.append(f"## `{table['table']}`")

        for field in table.get("fields", []):
            md.append(
                f"- `{field['name']}` → `{field['type']}`"
            )

    # =====================================================
    # FOLDER STRUCTURE
    # =====================================================

    md.append("\n# 📁 Folder Structure\n")

    md.append("```")
    md.append(data.get("folder_structure", ""))
    md.append("```")

    # =====================================================
    # TESTING
    # =====================================================

    md.append("\n# 🧪 Testing Strategy\n")
    md.append(data.get("testing_strategy", ""))

    # =====================================================
    # DEPLOYMENT
    # =====================================================

    md.append("\n# 🚀 Deployment Notes\n")
    md.append(data.get("deployment_notes", ""))

    return "\n".join(md)