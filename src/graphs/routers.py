from src.graphs.states import EngineeringState


def qa_router(state: EngineeringState):
    """
    Decide whether:
    - bugs need fixing
    - or delivery can happen
    """

    qa_report = state["qa_report"]

    if "FAILED" in qa_report:
        return "bug_fix"

    return "delivered"