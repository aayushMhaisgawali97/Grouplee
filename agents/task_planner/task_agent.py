from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Logic moved from GUI to API
def summarize_tasks(tasks):
    prompt = f"""You are a smart task planning agent.
Given a list of tasks, categorize them into 3 priority buckets:
- High Priority
- Medium Priority
- Low Priority

Tasks:
{tasks}

Return the response in this format:

High Priority:
- task 1
- task 2

Medium Priority:
- task 1
- task 2

Low Priority:
- task 1
- task 2
"""
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",  # Or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


@app.route('/')
def index():
    return render_template("landing.html")  # or "index.html"

@app.route('/task_planner')
def task_planner_page():
    return render_template("task_planner.html")  # HTML page with your task UI

@app.route('/task_planner', methods=['POST'])
def task_planner():
    data = request.get_json()
    tasks = data.get("text", "")
    result = summarize_tasks(tasks)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
