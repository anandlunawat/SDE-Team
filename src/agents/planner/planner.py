from src.graphs.states import EngineeringState
import src 


def planner_node(state: EngineeringState):
    print("\n--- PLANNER ---")

    task = state["user_request"]

    # Implement your planning logic here using src.client
    print(f"Planning for task: {task} using client: {src.client}")
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

    for part in src.client.chat('gpt-oss:120b-cloud', messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)

    # Collect the full plan output
    plan_output = ""
    for part in src.client.chat('gpt-oss:120b-cloud', messages=messages, stream=True):
        content = part['message']['content']
        plan_output += content
        print(content, end='', flush=True)

    return {
        "user_request": task,
        "architecture_plan": plan_output
    }
