"""LangGraph event processor for production-grade runtime orchestration."""
from typing import Any, Dict

from src.runtime.runtime_state import RuntimeState


def process_event(event: Dict[str, Any], runtime: RuntimeState) -> None:
    """Process a single LangGraph event and update the RuntimeState."""
    event_type = _get_event_type(event)
    node_name = _extract_node_name(event)
    print(f"Processing event: {event_type} for node: {node_name}")
    runtime.append_execution_trace({
        "event": event_type,
        "node": node_name,
        "data": _extract_trace_data(event),
    })

    if _is_chain_start(event_type):
        runtime.update_node_status(node_name or "unknown", "running")
        runtime.append_log(f"🔵 {node_name or 'Node'} started")
        print(f"Node {node_name or 'unknown'} started")
        return

    if _is_chain_end(event_type):
        runtime.update_node_status(node_name or "unknown", "completed")
        runtime.append_log(f"✅ {node_name or 'Node'} completed")
        print(f"Node {node_name or 'unknown'} completed")
        return

    if _is_chat_stream(event_type, event):
        chunk = _extract_token_chunk(event)
        print(f"Received token chunk for node {node_name or 'unknown'}: {chunk}")
        if chunk:
            target_node = node_name or runtime.get_state().get("current_node", "unknown")
            print(f"Appending chunk to node {target_node}: {chunk}")
            runtime.append_token(target_node, chunk)
        return

    if _is_state_snapshot(event_type, event):
        snapshot = _extract_state_snapshot(event)
        runtime.update_state_snapshot(snapshot)
        runtime.append_log("🧠 State snapshot updated")
        print(f"State snapshot updated for node {node_name or 'unknown'}")
        return

    if _is_interrupt(event_type, event):
        payload = _extract_interrupt_payload(event)
        runtime.set_interrupt(payload)
        runtime.append_log("⚠️ Interrupt received — approval required", level="warning")
        print(f"Interrupt received for node {node_name or 'unknown'}")
        return

    if event_type:
        print(f"Processing event: {event_type} for node: {node_name or 'unknown'}")
        runtime.append_log(f"🔔 Event: {event_type} received", level="debug")


def _get_event_type(event: Dict[str, Any]) -> str:
    print(f"Extracting event type from: {event}")
    return (
        str(event.get("event") or event.get("type") or event.get("name") or "").strip()
    )


def _extract_node_name(event: Dict[str, Any]) -> str:
    source_keys = ["node", "node_name", "chain", "chain_name", "name"]
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    for key in source_keys:
        if key in event and isinstance(event[key], str):
            return event[key]
        if key in data and isinstance(data[key], str):
            return data[key]
    if isinstance(event.get("stream"), dict):
        stream_data = event["stream"]
        for key in source_keys:
            if key in stream_data and isinstance(stream_data[key], str):
                return stream_data[key]
    return ""


def _extract_token_chunk(event: Dict[str, Any]) -> str:
    data = event.get("data") or {}
    if isinstance(data, dict):
        for key in ("chunk", "message", "content", "text", "delta"):
            if key in data:
                candidate = data[key]
                if isinstance(candidate, str):
                    return candidate
                if isinstance(candidate, dict) and "content" in candidate:
                    return str(candidate["content"])
    if isinstance(event.get("chunk"), str):
        return event["chunk"]
    return ""


def _extract_state_snapshot(event: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(event.get("data"), dict):
        return event["data"]
    if isinstance(event.get("snapshot"), dict):
        return event["snapshot"]
    if isinstance(event.get("values"), dict):
        return event["values"]
    return {}


def _extract_interrupt_payload(event: Dict[str, Any]) -> Any:
    data = event.get("data")
    if data is not None:
        return data
    if event.get("interrupts") is not None:
        return event.get("interrupts")
    if event.get("payload") is not None:
        return event.get("payload")
    return event


def _extract_trace_data(event: Dict[str, Any]) -> Any:
    data = event.get("data")
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in ("chunk", "message", "content", "delta")}
    return data


def _is_chain_start(event_type: str) -> bool:
    return event_type in {"on_chain_start", "chain_start", "node_start", "on_chain_start_event"}


def _is_chain_end(event_type: str) -> bool:
    return event_type in {"on_chain_end", "chain_end", "node_end", "on_chain_end_event"}


def _is_chat_stream(event_type: str, event: Dict[str, Any]) -> bool:
    if event_type in {"on_chat_model_stream", "chat_model_stream", "model_stream"}:
        return True
    return isinstance(event.get("data"), dict) and any(key in event["data"] for key in ("chunk", "message", "content", "text", "delta"))


def _is_state_snapshot(event_type: str, event: Dict[str, Any]) -> bool:
    return event_type in {"state_snapshot", "snapshot", "on_state_snapshot", "state_update"} or isinstance(event.get("values"), dict)


def _is_interrupt(event_type: str, event: Dict[str, Any]) -> bool:
    if event_type in {"stream.interrupted", "interrupt", "on_interrupt", "interrupted"}:
        return True
    stream_data = event.get("stream")
    return isinstance(stream_data, dict) and stream_data.get("interrupted") is True
