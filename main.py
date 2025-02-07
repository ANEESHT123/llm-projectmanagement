from flask import Flask, request, jsonify
from flask_cors import CORS
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
import types
import json

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize AI Model
llm = ChatOpenAI(model="gpt-4o")

# Project Manager Agent
project_manager = Agent(
    role="Project Manager",
    goal="Oversee project tasks and ensure efficient workflow",
    backstory="Experienced project manager with expertise in task allocation and team coordination",
    verbose=True,
    llm=llm
)

# Task Allocation Agent
task_allocator = Agent(
    role="Task Allocator",
    goal="Assign tasks to team members based on skills and workload",
    backstory="Strategic resource manager who optimizes task distribution",
    verbose=True,
    llm=llm
)

# Progress Tracking Agent
progress_tracker = Agent(
    role="Progress Tracker",
    goal="Monitor task progress and identify potential bottlenecks",
    backstory="Detailed-oriented analyst who keeps projects on track",
    verbose=True,
    llm=llm
)

# Create Tasks
def create_project_task(project_details):
    task = Task(
        description=f"Break down project details: {project_details} into specific tasks",
        agent=project_manager,
        expected_output="Detailed list of project tasks with priorities and estimated timelines"
    )
    return task

def allocate_tasks(task_list):
    task = Task(
        description=f"Allocate these tasks: {task_list} to appropriate team members",
        agent=task_allocator,
        expected_output="Task allocation plan with assigned team members and resources"
    )
    return task

def track_project_progress(allocated_tasks):
    task = Task(
        description=f"Track progress of tasks: {allocated_tasks}",
        agent=progress_tracker,
        expected_output="Comprehensive progress report with status updates and potential bottlenecks"
    )
    return task

# Convert the CrewOutput or TaskOutput object to a dictionary
def convert_to_dict(obj, visited=None):
    if visited is None:
        visited = set()

    if id(obj) in visited:
        return None
    visited.add(id(obj))

    if isinstance(obj, dict):
        return {key: convert_to_dict(value, visited) for key, value in obj.items()}
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('__') and not callable(value) and not isinstance(value, (types.GetSetDescriptorType, types.MemberDescriptorType)):
                result[key] = convert_to_dict(value, visited)
        return result
    elif isinstance(obj, list):
        return [convert_to_dict(item, visited) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_dict(item, visited) for item in obj)
    elif isinstance(obj, set):
        return {convert_to_dict(item, visited) for item in obj}
    else:
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            return str(obj)

# Create Crew
def manage_project(project_details):
    crew = Crew(
        agents=[project_manager, task_allocator, progress_tracker],
        tasks=[
            create_project_task(project_details),
            allocate_tasks(project_details),
            track_project_progress(project_details)
        ],
        verbose=True
    )
    result = crew.kickoff()

    # Ensure the result is serializable by converting it to a dict
    result_dict = convert_to_dict(result)
    
    return result_dict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


@app.route('/manage-project', methods=['POST'])
def manage_project_endpoint():
    project_details = request.json.get('project_details')
    result = manage_project(project_details)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)