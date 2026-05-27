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
            "node_status": {},              # {"planner": "running", "architect": "pending", ...}
            "streamed_tokens": {},          # {"planner": "token1token2...", "architect": "...", ...}
            "logs": [],                     # [{"timestamp": "...", "level": "info", "message": "..."}, ...]
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
            self._state["error"] = None
    
    def set_workflow_completed(self, final_state: Optional[Dict[str, Any]] = None) -> None:
        """Mark workflow as completed and optionally store final state."""
        with self._state_lock:
            self._state["workflow_completed"] = True
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
                "node_status": self._state["node_status"].copy(),
                "streamed_tokens": self._state["streamed_tokens"].copy(),
                "logs": self._state["logs"].copy(),
                "workflow_started": self._state["workflow_started"],
                "workflow_completed": self._state["workflow_completed"],
                "error": self._state["error"],
                "final_state": self._state["final_state"].copy(),
            }
    
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
                "node_status": {},
                "streamed_tokens": {},
                "logs": [],
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
