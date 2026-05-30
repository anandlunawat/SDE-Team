from src.graphs.states import EngineeringState
from langgraph.types import interrupt
import src
import json

from src.runtime.streaming import set_interrupt

def architecture_approval_node(state: EngineeringState):
    print("\n--- ARCHITECTURE APPROVAL AGENT ---")

    # =====================================================
    # EXTRACT ARCHITECTURE TASKS
    # =====================================================

    set_interrupt(payload= {
        "type": "architecture_approval",
        "message": "Do you approve the proposed architecture?"
    })

    approval = interrupt("Approval needed for architecture. Do you approve the proposed architecture? (yes/no)")

    return {
        "architecture_approval": approval
    }
