"""SDE Team Project"""
import argparse
import os
from dotenv import load_dotenv
from ollama import Client

from src.graphs.states import EngineeringState
from src.graphs.engineering_graph import buildGraph

# Load environment variables from .env file
load_dotenv()

# print(os.environ.get('OLLAMA_API_KEY'))

client = None

def get_client():
  global client
  if client is not None:
    return client
  newClient = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
  )
  client = newClient

def run(app, initial_state: EngineeringState):
    # =========================================================
    # RUN
    # =========================================================
    
    result = app.invoke(initial_state)
    
    # =========================================================
    # OUTPUT
    # =========================================================
    
    print("\n\n================ FINAL RESULT ================\n")
    
    for key, value in result.items():
        print(f"\n{key}:\n{value}")

def main():
    # Example usage of the client
    get_client()
    parser = argparse.ArgumentParser(description="SDE Team Project")
    parser.add_argument('--task', type=str, help='Task to be planned')
    args = parser.parse_args()
    task = args.task
    if task:
        print(f"Planning for task: {task}")

        app = buildGraph()
        
        # Initialize EngineeringState with the task
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
        
        print("Engineering State initialized:", initial_state)
        
        # Run the workflow with the initial state
        run(app, initial_state)
        
        # Here you can create an instance of Planner and call the plan method
        # planner = Planner(task, newClient)
    else:
        print("No task provided. Please use --task to specify a task.")

if __name__ == "__main__":
    main()

__all__ = ["client"]