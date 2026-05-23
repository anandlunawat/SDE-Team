from src.graphs.states import EngineeringState


def reviewer_node(state: EngineeringState):
    print("\n--- REVIEWER ---")

    frontend = state.get("frontend_code", "")
    backend = state.get("backend_code", "")

    return {
        "review_feedback": f"""
        Reviewed frontend:
        {frontend}

        Reviewed backend:
        {backend}

        Minor issues found.
"""
    }

