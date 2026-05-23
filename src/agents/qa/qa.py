from src.graphs.states import EngineeringState


def qa_node(state: EngineeringState):
    print("\n--- QA TESTING ---")

    iteration = state.get("iteration", 0)

    # Simulating first QA failure
    if iteration < 1:
        return {
            "qa_report": "QA FAILED: API response mismatch",
            "iteration": iteration + 1
        }

    return {
        "qa_report": "QA PASSED"
    }
