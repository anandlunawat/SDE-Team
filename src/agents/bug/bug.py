from src.graphs.states import EngineeringState


def bug_fix_node(state: EngineeringState):
    print("\n--- BUG FIX AGENT ---")

    qa_report = state["qa_report"]

    return {
        "bug_fixed_code": f"Fixed issues from QA report: {qa_report}"
    }
