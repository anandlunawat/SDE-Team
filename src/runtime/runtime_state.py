"""Thread-safe RuntimeState manager for background graph execution and realtime UI streaming."""
import threading
from typing import Any, Dict, List, Optional
from datetime import datetime


class RuntimeState:
    """
    Thread-safe singleton for managing workflow execution state.
    
    Decouples LangGraph execution (background thread) from Streamlit UI (render thread).
    All state mutations are protected by threading.Lock for consistency.
    
    Architecture:
        Background LangGraph Thread → RuntimeState (write)
        Streamlit UI Thread → RuntimeState (read snapshots)
    """
    
    _instance: Optional['RuntimeState'] = None
    _lock: threading.Lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern with thread-safe instantiation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize runtime state once."""
        if self._initialized:
            return
        
        self._state_lock = threading.Lock()
        self._state: Dict[str, Any] = {
            "user_request": "",
            "current_node": "",
            "workflow_status": "idle",
            "node_status": {},              # {"planner": "running", "architect": "pending", ...}
            "streamed_tokens": {},          # {"planner": "token1token2...", "architect": "...", ...}
            "logs": [],                     # [{"timestamp": "...", "level": "info", "message": "..."}, ...]
            "latest_state_snapshot": {},
            "interrupts": [],
            "pending_interrupt": None,
            "resume_response": None,
            "execution_trace": [],
            "workflow_started": False,
            "workflow_completed": False,
            "error": None,
            "final_state": {},
        }
        self._initialized = True
    
    def update_node_status(self, node_name: str, status: str) -> None:
        """
        Update the status of a node (pending, running, completed, error).
        
        Args:
            node_name: Name of the node (e.g., "planner", "architect")
            status: Status value (e.g., "pending", "running", "completed", "error")
        """
        with self._state_lock:
            self._state["node_status"][node_name] = status
            self._state["current_node"] = node_name
    
    def append_token(self, node_name: str, token: str) -> None:
        """
        Append a token/chunk to the stream for a specific node.
        Thread-safe streaming of LLM output.
        
        Args:
            node_name: Name of the node (e.g., "planner", "architect")
            token: Token/chunk to append to the stream
        """
        with self._state_lock:
            if node_name not in self._state["streamed_tokens"]:
                self._state["streamed_tokens"][node_name] = ""
            self._state["streamed_tokens"][node_name] += token
    
    def append_log(self, message: str, level: str = "info") -> None:
        """
        Append a log message with timestamp.
        
        Args:
            message: Log message
            level: Log level (info, warning, error, success, debug)
        """
        with self._state_lock:
            self._state["logs"].append({
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message
            })
    
    def set_error(self, error_msg: str) -> None:
        """
        Set error state and log the error.
        
        Args:
            error_msg: Error message
        """
        with self._state_lock:
            self._state["error"] = error_msg
            self._state["workflow_status"] = "error"
        self.append_log(f"ERROR: {error_msg}", level="error")
    
    def clear_error(self) -> None:
        """Clear error state."""
        with self._state_lock:
            self._state["error"] = None
    
    def set_workflow_started(self, user_request: str) -> None:
        """Mark workflow as started and store user request."""
        with self._state_lock:
            self._state["user_request"] = user_request
            self._state["workflow_started"] = True
            self._state["workflow_completed"] = False
            self._state["workflow_status"] = "running"
            self._state["error"] = None
    
    def set_workflow_completed(self, final_state: Optional[Dict[str, Any]] = None) -> None:
        """Mark workflow as completed and optionally store final state."""
        with self._state_lock:
            self._state["workflow_completed"] = True
            self._state["workflow_status"] = "completed"
            if final_state:
                self._state["final_state"] = final_state
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get a snapshot of current state (thread-safe read).
        Returns a copy to prevent external mutations.
        
        Returns:
            Current state snapshot
        """
        with self._state_lock:
            return {
                "user_request": self._state["user_request"],
                "current_node": self._state["current_node"],
                "workflow_status": self._state["workflow_status"],
                "node_status": self._state["node_status"].copy(),
                "streamed_tokens": self._state["streamed_tokens"].copy(),
                "logs": self._state["logs"].copy(),
                "latest_state_snapshot": self._state["latest_state_snapshot"].copy(),
                "interrupts": self._state["interrupts"].copy(),
                "pending_interrupt": self._state["pending_interrupt"],
                "resume_response": self._state["resume_response"],
                "execution_trace": self._state["execution_trace"].copy(),
                "workflow_started": self._state["workflow_started"],
                "workflow_completed": self._state["workflow_completed"],
                "error": self._state["error"],
                "final_state": self._state["final_state"].copy(),
            }

    def append_execution_trace(self, entry: Dict[str, Any]) -> None:
        """Append a structured event to the execution trace."""
        with self._state_lock:
            self._state["execution_trace"].append(entry)

    def update_state_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """Store the latest graph state snapshot."""
        with self._state_lock:
            self._state["latest_state_snapshot"] = snapshot.copy() if isinstance(snapshot, dict) else snapshot
            self._state["execution_trace"].append({
                "event": "state_snapshot",
                "snapshot": snapshot,
            })

    def set_interrupt(self, payload: Any) -> None:
        """Store an interrupt payload and pause workflow execution."""
        with self._state_lock:
            self._state["pending_interrupt"] = payload
            self._state["interrupts"].append(payload)
            self._state["workflow_status"] = "paused"

    def clear_interrupt(self) -> None:
        """Clear the pending interrupt payload."""
        with self._state_lock:
            self._state["pending_interrupt"] = None

    def set_resume_response(self, response: Any) -> None:
        """Store the user resume response for an interrupted workflow."""
        with self._state_lock:
            self._state["resume_response"] = response

    def get_resume_response(self) -> Any:
        """Get the current resume response."""
        with self._state_lock:
            return self._state["resume_response"]

    def clear_resume_response(self) -> None:
        """Clear any stored resume response."""
        with self._state_lock:
            self._state["resume_response"] = None

    def has_pending_interrupt(self) -> bool:
        """Return whether a workflow interrupt is currently pending."""
        with self._state_lock:
            return self._state["pending_interrupt"] is not None

    def set_workflow_status(self, status: str) -> None:
        """Set a normalized workflow status string."""
        with self._state_lock:
            self._state["workflow_status"] = status

    def get_pending_interrupt(self) -> Any:
        """Return the pending interrupt payload."""
        with self._state_lock:
            return self._state["pending_interrupt"]

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Return a copy of the execution trace."""
        with self._state_lock:
            return self._state["execution_trace"].copy()

    def get_latest_state_snapshot(self) -> Dict[str, Any]:
        """Return the latest state snapshot."""
        with self._state_lock:
            return self._state["latest_state_snapshot"].copy()

    def get_workflow_status(self) -> str:
        """Return the current workflow status."""
        with self._state_lock:
            return self._state["workflow_status"]

    def get_node_tokens(self, node_name: str) -> str:
        """
        Get all streamed tokens for a specific node.
        
        Args:
            node_name: Name of the node
            
        Returns:
            Concatenated token stream for the node
        """
        with self._state_lock:
            return self._state["streamed_tokens"].get(node_name, "")
    
    def get_node_status(self, node_name: str) -> str:
        """
        Get the status of a specific node.
        
        Args:
            node_name: Name of the node
            
        Returns:
            Status string or "pending" if not found
        """
        with self._state_lock:
            return self._state["node_status"].get(node_name, "pending")
    
    def reset(self) -> None:
        """Reset entire runtime state (for new workflow)."""
        with self._state_lock:
            self._state = {
                "user_request": "",
                "current_node": "",
                "workflow_status": "idle",
                "node_status": {},
                "streamed_tokens": {},
                "logs": [],
                "latest_state_snapshot": {},
                "interrupts": [],
                "pending_interrupt": None,
                "resume_response": None,
                "execution_trace": [],
                "workflow_started": False,
                "workflow_completed": False,
                "error": None,
                "final_state": {},
            }
    
    def is_workflow_running(self) -> bool:
        """Check if workflow is currently running."""
        with self._state_lock:
            return self._state["workflow_started"] and not self._state["workflow_completed"]


# Global singleton instance
runtime_state = RuntimeState()
