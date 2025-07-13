from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Utility to extract text from uploaded files
def extract_text(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ext = os.path.splitext(filename)[1].lower()
    content = ""

    if ext == ".pdf":
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content += page.extract_text() or ""
    elif ext == ".docx":
        doc = Document(filepath)
        for para in doc.paragraphs:
            content += para.text + "\n"
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        raise ValueError("Unsupported file format.")

    return content.strip()

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    return render_template("landing.html")

@app.route('/task-planner')
def task_planner_page():
    return render_template("task_planner.html")

@app.route('/assessment_agent')
def assessment_agent_page():
    return render_template("assessment_agent.html")

@app.route('/summarizer-agent')
def summarizer_agent_page():
    return render_template("summarizer_agent.html")

@app.route('/content-generator')
def content_generator_page():
    return render_template("content_generator.html")

@app.route('/insight-generator')
def insight_generator_page():
    return render_template("insight_generator.html")


# --------- Task Planner AI Endpoint --------- #
@app.route('/task_planner', methods=['POST'])
def task_planner_ai():
    data = request.json
    task_input = data.get("text", "")

    prompt = f"""You are a smart task planning agent.
Given a list of tasks, categorize them into 3 priority buckets:
- High Priority
- Medium Priority
- Low Priority

Tasks:
{task_input}

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

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"❌ Error: {str(e)}"})

# --------- Assessment Agent AI Endpoint --------- #
@app.route('/assessment_agent', methods=['POST'])
def assessment_agent_ai():
    try:
        if 'file' in request.files and request.files['file'].filename:
            content = extract_text(request.files['file'])
        else:
            content = request.form.get("text", "").strip()

        difficulty = request.form.get("difficulty", "medium")

        if not content:
            return jsonify({"feedback": "❌ No valid input provided."})

        prompt = f"""You are an AI assistant that generates quiz questions for students.

Based on the following study material:

"{content}"

Create a structured short assessment including:
- 3 multiple choice questions (each with 4 options and the correct answer)
- 2 short answer questions
- 1 higher-order thinking question that promotes critical thinking

Also provide a short feedback summary of the content at the end.

Format your output clearly like this:

📘 Multiple Choice Questions:
1. Question?
   a) Option A
   b) Option B
   c) Option C
   d) Option D  
   ✅ Answer: X

🖊️ Short Answer Questions:
1. Question?
2. Question?

🧠 Higher Order Thinking:
- Question?

📝 Feedback:
<Your summary or guidance>
"""

        response = client.chat.completions.create(
            model= "gpt-4.1-nano-2025-04-14",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content.strip()

        questions, feedback = "", result
        if "Feedback:" in result:
            parts = result.split("Feedback:")
            questions = parts[0].strip()
            feedback = "Feedback:" + parts[1].strip()

        return jsonify({
            "questions": questions,
            "feedback": feedback
        })

    except Exception as e:
        return jsonify({"feedback": f"❌ Error: {str(e)}"})

# --------- Summarizer Agent AI Endpoint --------- #
@app.route('/summarize', methods=['POST'])
def summarize_agent():
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file uploaded."})

        file = request.files['file']
        content = extract_text(file)

        prompt = f"""You are a professional summarizer.
Please summarize the following text clearly and concisely:

{content}

Summary:"""

        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"})

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)


@app.route('/moderator', methods=['POST'])
def moderator():
    try:
        task = request.json.get("task", "")
        if not task:
            return jsonify({"error": "❌ No task provided."})

        # Use GPT to decide which agent to call
        decision_prompt = f"""You are a smart AI moderator.
Given the following user request, decide which agent should handle it.

Agents:
1. summarizer - Summarizes documents or text
2. assessment_agent - Generates quiz questions from content
3. task_planner - Organizes a list of tasks into priorities

User Task:
\"\"\"{task}\"\"\"

Respond ONLY with the agent name: summarizer, assessment_agent, or task_planner."""

        decision = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": decision_prompt}]
        ).choices[0].message.content.strip().lower()

        if "summarizer" in decision:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": f"Summarize this:\n{task}"}]
            )
            result = response.choices[0].message.content.strip()
            return jsonify({"agent_used": "summarizer", "output": result})

        elif "assessment" in decision:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": f"Generate quiz from this:\n{task}"}]
            )
            result = response.choices[0].message.content.strip()
            return jsonify({"agent_used": "assessment_agent", "output": result})

        elif "task_planner" in decision:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": f"Plan tasks:\n{task}"}]
            )
            result = response.choices[0].message.content.strip()
            return jsonify({"agent_used": "task_planner", "output": result})

        else:
            return jsonify({"error": f"❌ Couldn't identify a matching agent from: {decision}"})

    except Exception as e:
        return jsonify({"error": f"❌ Moderator error: {str(e)}"})
