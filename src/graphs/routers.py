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

def architecture_approval_router(state: EngineeringState):
    """
    Decide whether:
    - backend architecture needs to be revised
    - or we can proceed with development
    """

    approval = state["architecture_approval"]

    if approval == "no":
        return "architect"

    return "frontend"