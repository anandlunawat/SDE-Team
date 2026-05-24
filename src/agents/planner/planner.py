from src.graphs.states import EngineeringState
import src
from src.runtime.streaming import (
    update_node_status,
    append_stream_token,
    append_log
)


def planner_node(state: EngineeringState):
    task = state["user_request"]
    
    update_node_status("planner", "running")
    append_log("🔵 Planner started analyzing task")

    messages = [
        {
            "role": "system",
            "content": """
        You are an expert AI Software Engineering Planner.

        Your responsibility is to analyze the given software development task
        and create a highly detailed execution plan for an autonomous AI
        engineering team.

        The plan will later be executed by:
        - Architect Agent
        - Frontend Agent
        - Backend Agent
        - QA Agent
        - Reviewer Agent

        You must:
        1. Understand the business requirement
        2. Break the task into smaller actionable subtasks
        3. Define frontend requirements
        4. Define backend requirements
        5. Define API requirements
        6. Define database requirements if needed
        7. Mention authentication requirements if applicable
        8. Mention edge cases
        9. Mention testing requirements
        10. Mention deployment considerations

        Return the response in the following structured format:

        # Project Goal

        # Functional Requirements

        # Edge Cases

        # QA Test Cases

        # Deployment Notes

        Keep the plan technical, structured, and implementation-ready.
        Do not write vague high-level descriptions.
        """
        },
        {
            "role": "user",
            "content": f"""
        Create a detailed engineering execution plan for the following task:

        TASK:
        {task}
        """
        },
    ]

    plan_output = ""
    for part in src.client.chat('gpt-oss:120b-cloud', messages=messages, stream=True):
        content = part['message']['content']
        plan_output += content
        append_stream_token("planner", content)
        print(content, end="", flush=True)

    update_node_status("planner", "completed")
    append_log("✅ Planner completed")

    return {
        "user_request": task,
        "architecture_plan": plan_output
    }
