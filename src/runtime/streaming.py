"""Streaming state manager for realtime LangGraph orchestration in Streamlit."""
import streamlit as st
from typing import Any, Dict, List


def initialize_streaming_state():
    """Initialize streaming state in st.session_state if not present."""
    if "engineering_state" not in st.session_state:
        st.session_state.engineering_state = {
            "user_request": "",
            "current_node": "",
            "node_status": {},  # {"planner": "completed", "architect": "running", ...}
            "streamed_tokens": {},  # {"planner": "token1token2...", "architect": "..."}
            "logs": [],  # [(timestamp, level, message), ...]
            "final_state": {},
            "graph_output_buffer": {},  # raw graph output
            "error": None,
            "workflow_started": False,
            "workflow_completed": False,
        }


def update_node_status(node_name: str, status: str):
    """Update the status of a node (pending, running, completed, error).
    
    Args:
        node_name: Name of the node (e.g., "planner", "architect")
        status: Status (e.g., "pending", "running", "completed", "error")
    """
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    st.session_state.engineering_state["node_status"][node_name] = status
    st.session_state.engineering_state["current_node"] = node_name


def append_stream_token(node_name: str, token: str):
    """Append a token to the stream for a specific node.
    
    Args:
        node_name: Name of the node (e.g., "planner", "architect")
        token: Token/chunk to append
    """
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    if node_name not in st.session_state.engineering_state["streamed_tokens"]:
        st.session_state.engineering_state["streamed_tokens"][node_name] = ""
    
    st.session_state.engineering_state["streamed_tokens"][node_name] += token


def append_log(message: str, level: str = "info"):
    """Append a log message.
    
    Args:
        message: Log message
        level: Log level (info, warning, error, success)
    """
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    st.session_state.engineering_state["logs"].append({
        "level": level,
        "message": message
    })


def set_error(error_msg: str):
    """Set error state."""
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    st.session_state.engineering_state["error"] = error_msg
    append_log(f"ERROR: {error_msg}", level="error")


def clear_error():
    """Clear error state."""
    if "engineering_state" in st.session_state:
        st.session_state.engineering_state["error"] = None


def set_final_state(state: Dict[str, Any]):
    """Store the final state from the graph."""
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    st.session_state.engineering_state["final_state"] = state


def get_streaming_state() -> Dict[str, Any]:
    """Get the current streaming state."""
    if "engineering_state" not in st.session_state:
        initialize_streaming_state()
    
    return st.session_state.engineering_state


def get_node_tokens(node_name: str) -> str:
    """Get all streamed tokens for a specific node."""
    state = get_streaming_state()
    return state["streamed_tokens"].get(node_name, "")


def get_node_status(node_name: str) -> str:
    """Get the status of a specific node."""
    state = get_streaming_state()
    return state["node_status"].get(node_name, "pending")


def reset_streaming_state():
    """Reset the entire streaming state (for new workflow)."""
    if "engineering_state" in st.session_state:
        st.session_state.engineering_state = {
            "user_request": "",
            "current_node": "",
            "node_status": {},
            "streamed_tokens": {},
            "logs": [],
            "final_state": {},
            "graph_output_buffer": {},
            "error": None,
            "workflow_started": False,
            "workflow_completed": False,
        }
