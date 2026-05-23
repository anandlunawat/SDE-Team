from src.graphs.states import EngineeringState


def delivery_node(state: EngineeringState):
    print("\n--- DELIVERY ---")

    return {
        "delivered": True
    }