import os
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from openai import OpenAI
from docx import Document
import PyPDF2

# Load OpenAI API key from .env file
load_dotenv(dotenv_path="../.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load prompt template from external text file
def load_template():
    try:
        with open("prompt_template.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Error: 'prompt_template.txt' not found.")
        exit()


# Read content from .pdf, .docx, or .txt file
def read_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    content = ""

    if ext == ".pdf":
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
    elif ext == ".docx":
        doc = Document(filepath)
        for para in doc.paragraphs:
            content += para.text + "\n"
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
    else:
        raise ValueError("Unsupported file type.")
    
    return content.strip()

# Send content to OpenAI and generate assessment
def generate_assessment(content):
    prompt = load_template().format(content=content)
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    
    return response.choices[0].message.content.strip()

# Show a GUI file picker
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your notes file",
        filetypes=[("Documents", "*.pdf *.docx *.txt")]
    )
    return file_path

# Main execution
if __name__ == "__main__":
    filepath = select_file()

    if not filepath:
        print("❌ No file selected.")
        exit()

    try:
        content = read_document(filepath)
        if not content:
            print("❌ Document is empty.")
        else:
            print(f"\n📘 File selected: {filepath}")
            print("🧠 Generating assessment...\n")
            result = generate_assessment(content)
            print("✅ Assessment:\n")
            print(result)

    except Exception as e:
        print(f"❌ Error: {e}")
