from summarizer_agent import SummarizerAgent

def run():
    agent = SummarizerAgent()

    # PDF test
    pdf_summary = agent.summarize_pdf("sample.pdf")
    print("\n📄 PDF Summary:\n", pdf_summary)

    # Paragraph test
    paragraph = """
    Artificial intelligence is rapidly changing how we live and work.
    It powers automation, smart assistants, autonomous vehicles,
    and countless other applications.
    """
    para_summary = agent.summarize_text(paragraph)
    print("\n📜 Paragraph Summary:\n", para_summary)

if __name__ == "__main__":
    run()
