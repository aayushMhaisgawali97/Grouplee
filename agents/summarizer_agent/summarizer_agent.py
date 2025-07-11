import os
from dotenv import load_dotenv, find_dotenv
import pdfplumber

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load .env
load_dotenv(find_dotenv())

class SummarizerAgent:
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("❌ OPENAI_API_KEY not found! Check your .env file.")
        print(f"✅ Using OpenAI key: {openai_key[:8]}...")

        self.llm = ChatOpenAI(
            model_name="gpt-4.1-nano-2025-04-14",
            temperature=0.3,
            openai_api_key=openai_key
        )

    def summarize_text(self, text):
        prompt = PromptTemplate(
            input_variables=["content"],
            template="""
You are a professional summarizer.
Please summarize the following text clearly and concisely:

{content}

Summary:
"""
        )

        chain = prompt | self.llm
        result = chain.invoke({"content": text[:6000]})
        return result.content

    def summarize_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return self.summarize_text(text)