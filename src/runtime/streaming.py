"""Streaming interface layer - thin wrapper around RuntimeState for backward compatibility."""
from src.runtime.runtime_state import runtime_state


def initialize_streaming_state():
    """No-op for backward compatibility. RuntimeState is auto-initialized."""
    pass


def update_node_status(node_name: str, status: str):
    """Update the status of a node."""
    runtime_state.update_node_status(node_name, status)


def append_stream_token(node_name: str, token: str):
    """Append a token to the stream for a specific node."""
    runtime_state.append_token(node_name, token)


def append_log(message: str, level: str = "info"):
    """Append a log message."""
    runtime_state.append_log(message, level)


def set_error(error_msg: str):
    """Set error state."""
    runtime_state.set_error(error_msg)


def clear_error():
    """Clear error state."""
    runtime_state.clear_error()


def set_final_state(state: dict):
    """Store the final state from the graph."""
    runtime_state.set_workflow_completed(state)


def get_streaming_state() -> dict:
    """Get the current streaming state snapshot."""
    return runtime_state.get_state()


def get_node_tokens(node_name: str) -> str:
    """Get all streamed tokens for a specific node."""
    return runtime_state.get_node_tokens(node_name)


def get_node_status(node_name: str) -> str:
    """Get the status of a specific node."""
    return runtime_state.get_node_status(node_name)


def reset_streaming_state():
    """Reset the entire streaming state (for new workflow)."""
    runtime_state.reset()


def get_streamed_tokens() -> dict:
    """Get all streamed tokens for every node."""
    state = runtime_state.get_state()
    return state.get("streamed_tokens", {})
