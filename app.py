"""Streamlit UI-first Realtime LangGraph Orchestration Dashboard"""
import streamlit as st
import time
import threading
from src.graphs.engineering_graph import buildGraph
from src.graphs.states import EngineeringState
from src.runtime.streaming import (
    initialize_streaming_state,
    get_streaming_state,
    reset_streaming_state,
    append_log
)
from src.runtime.runtime_state import runtime_state


def initialize_app():
    """Initialize app state and graph on startup."""
    initialize_streaming_state()
    
    if "graph" not in st.session_state:
        st.session_state.graph = buildGraph()
        append_log("✅ Graph initialized")
    
    # Setup periodic rerun for live updates
    if "rerun_counter" not in st.session_state:
        st.session_state.rerun_counter = 0


def render_sidebar():
    """Render sidebar with task input and controls."""
    st.sidebar.title("🤖 AI Engineering Team")
    
    # Task input
    task = st.sidebar.text_area(
        "📝 Enter your engineering task:",
        value="Build an AI powered ecommerce application",
        height=120,
        key="task_input"
    )
    
    # Start button
    start_col, reset_col = st.sidebar.columns(2)
    
    with start_col:
        start_clicked = st.button(
            "🚀 Start Workflow",
            type="primary",
            use_container_width=True
        )
    
    with reset_col:
        reset_clicked = st.button(
            "🔄 Reset",
            use_container_width=True
        )
    
    return task, start_clicked, reset_clicked


def render_header():
    """Render header section."""
    st.title("🤖 AI Engineering Team Dashboard")
    st.markdown("### Autonomous AI-Powered Engineering Orchestration")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    state = get_streaming_state()
    
    with col1:
        st.metric("Current Node", state.get("current_node", "—"))
    
    with col2:
        completed = len([s for s in state.get("node_status", {}).values() if s == "completed"])
        st.metric("Completed Nodes", completed)
    
    with col3:
        logs_count = len(state.get("logs", []))
        st.metric("Total Logs", logs_count)
    
    with col4:
        status = "✅ Idle"
        if state.get("workflow_started") and not state.get("workflow_completed"):
            status = "🔄 Running"
        elif state.get("workflow_completed"):
            status = "✅ Completed"
        st.metric("Status", status)


def render_node_status():
    """Render node status visualization."""
    st.subheader("📊 Workflow Progress")
    
    state = get_streaming_state()
    node_status = state.get("node_status", {})
    
    # Status mapping
    status_emoji = {
        "pending": "⏳",
        "running": "🔄",
        "completed": "✅",
        "error": "❌"
    }
    
    cols = st.columns(len(node_status) if node_status else 1)
    
    if node_status:
        for idx, (node, status_val) in enumerate(node_status.items()):
            with cols[idx % len(cols)]:
                emoji = status_emoji.get(status_val, "—")
                st.write(f"{emoji} **{node.capitalize()}**")
                st.caption(status_val)
    else:
        st.info("Waiting for workflow to start...")


def render_live_tokens():
    """Render live streamed tokens from nodes."""
    st.subheader("📡 Live Token Stream")
    
    state = get_streaming_state()
    streamed_tokens = state.get("streamed_tokens", {})
    
    if not streamed_tokens:
        st.info("Waiting for agent responses...")
        return
    
    # Create tabs for each node
    tabs = st.tabs([node.capitalize() for node in streamed_tokens.keys()])
    
    for tab, (node, tokens) in zip(tabs, streamed_tokens.items()):
        with tab:
            if tokens:
                st.markdown(tokens)
            else:
                st.caption(f"Waiting for {node} output...")


def render_logs():
    """Render workflow logs."""
    st.subheader("📝 Workflow Logs")
    
    state = get_streaming_state()
    logs = state.get("logs", [])
    
    if not logs:
        st.caption("No logs yet...")
        return
    
    # Reverse to show latest first
    for log in reversed(logs[-20:]):  # Show last 20 logs
        level = log.get("level", "info")
        message = log.get("message", "")
        
        if level == "error":
            st.error(message)
        elif level == "warning":
            st.warning(message)
        elif level == "success":
            st.success(message)
        else:
            st.info(message)


def run_graph_in_background(task: str, graph):
    """
    Execute graph in a background thread.
    
    Graph execution streams tokens/logs to RuntimeManager.
    UI polls RuntimeManager independently.
    
    Args:
        task: User's engineering task
        graph: Compiled LangGraph instance
    """
    try:
        # Mark workflow as started
        runtime_state.set_workflow_started(task)
        append_log("🚀 Workflow started")
        
        # Create initial state
        initial_state: EngineeringState = {
            "user_request": task,
            "architecture_plan": "",
            "tasks": [],
            "active_task": {},
            "completed_tasks": [],
            "generated_code": "",
            "review_feedback": "",
            "review_approved": False,
            "test_results": "",
            "test_passed": False,
            "errors": [],
            "debug_attempts": 0,
            "modified_files": [],
            "project_context": ""
        }
        
        # Stream graph execution (non-blocking)
        for event in graph.stream(initial_state):
            # Graph nodes update RuntimeManager directly
            # No need to do anything here - just let it stream
            pass
        
        # Mark workflow as completed
        runtime_state.set_workflow_completed(initial_state)
        append_log("✅ Workflow completed successfully")
        
    except Exception as e:
        error_msg = f"❌ Workflow failed: {str(e)}"
        runtime_state.set_error(error_msg)
        append_log(error_msg, level="error")


def run_workflow(task: str):
    """
    Initiate background graph execution (non-blocking).
    
    This starts a daemon thread and returns immediately.
    UI will poll RuntimeManager for updates.
    """
    # Start graph execution in background thread
    graph_thread = threading.Thread(
        target=run_graph_in_background,
        args=(task, st.session_state.graph),
        daemon=True
    )
    graph_thread.start()
    
    # Return immediately - Streamlit will rerun periodically to poll RuntimeManager
    st.session_state.workflow_thread = graph_thread


def main():
    """Main Streamlit app entry point."""
    # Page config
    st.set_page_config(
        page_title="AI Engineering Team",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize
    initialize_app()
    
    # Sidebar
    task, start_clicked, reset_clicked = render_sidebar()
    
    # Handle reset
    if reset_clicked:
        reset_streaming_state()
        st.rerun()
    
    # Main area
    render_header()
    
    st.divider()
    
    render_node_status()
    
    st.divider()
    
    # Start workflow if button clicked
    if start_clicked:
        run_workflow(task)
    
    # Render live content (always visible)
    render_live_tokens()
    st.divider()
    render_logs()
    
    # Poll RuntimeManager for updates every 0.5 seconds
    state = runtime_state.get_state()
    if state.get("workflow_started") and not state.get("workflow_completed"):
        time.sleep(0.5)
        st.rerun()


if __name__ == "__main__":
    main()

