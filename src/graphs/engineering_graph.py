from langgraph.graph import StateGraph

from src.agents.architecture.architect import architect_node
from src.agents.backend.backend import backend_node
from src.agents.bug.bug import bug_fix_node
from src.agents.delivery.delivery import delivery_node
from src.agents.frontend.frontend import frontend_node
from src.agents.planner.planner import planner_node
from src.agents.qa.qa import qa_node
from src.agents.reviewer.reviewer import reviewer_node
from src.graphs.routers import qa_router
from src.graphs.states import EngineeringState

from langgraph.graph import StateGraph, END



def buildGraph() :
    # =========================================================
    # BUILD GRAPH
    # =========================================================

    graph = StateGraph(EngineeringState)


    # =========================================================
    # ADD NODES
    # =========================================================

    graph.add_node("planner", planner_node)

    graph.add_node("architect", architect_node)

    graph.add_node("frontend", frontend_node)

    graph.add_node("backend", backend_node)

    graph.add_node("reviewer", reviewer_node)

    graph.add_node("qa_testing", qa_node)

    graph.add_node("bug_fix", bug_fix_node)

    graph.add_node("delivered", delivery_node)


    # =========================================================
    # ENTRY POINT
    # =========================================================

    graph.set_entry_point("planner")


    # =========================================================
    # MAIN FLOW
    # =========================================================

    graph.add_edge("planner", "architect")


    # =========================================================
    # SEQUENTIAL EXECUTION (architect → frontend → backend)
    # Sequential prevents threading issues with Streamlit streaming.
    # For true parallel with live UI, implement thread-safe buffers.
    # =========================================================

    graph.add_edge("architect", "frontend")
    graph.add_edge("frontend", "backend")


    # =========================================================
    # MERGE TO REVIEWER
    # =========================================================

    graph.add_edge("backend", "reviewer")


    # =========================================================
    # REVIEW → QA
    # =========================================================

    graph.add_edge("reviewer", "qa_testing")


    # =========================================================
    # CONDITIONAL QA ROUTING
    # =========================================================

    graph.add_conditional_edges(
        "qa_testing",
        qa_router,
        {
            "bug_fix": "bug_fix",
            "delivered": "delivered"
        }
    )


    # =========================================================
    # BUG FIX LOOP
    # =========================================================

    graph.add_edge("bug_fix", "reviewer")


    # =========================================================
    # FINISH POINT
    # =========================================================

    graph.add_edge("delivered", END)


    # =========================================================
    # COMPILE
    # =========================================================

    app = graph.compile()

    return app


