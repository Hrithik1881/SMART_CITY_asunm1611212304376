import gradio as gr
from PyPDF2 import PdfReader
import google.generativeai as genai

# ---------------- Setup Gemini Client ----------------
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # ⚠️ Replace with your own key
genai.configure(api_key=GOOGLE_API_KEY)

# Use Gemini 1.5 Flash (fast, optimized)
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- Response Generator ----------------
def generate_response(prompt, max_length=80):
    """
    Generate short, clear, human-readable responses.
    Streaming enabled for lower latency.
    """
    try:
        stream = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_length,
                temperature=0.2,  # deterministic, concise
            ),
            stream=True,
        )

        response_text = "".join(chunk.text for chunk in stream if chunk.text)
        return response_text.strip() if response_text else "No response."
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- PDF Text Extraction ----------------
def extract_text_from_pdf(pdf_file):
    """
    Extracts raw text from a PDF file.
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# ---------------- Eco Tips Generator ----------------
def eco_tips_generator(problem_keywords):
    prompt = (
        f"Give 3 very short eco-friendly tips about {problem_keywords}. "
        f"Each tip must be max 1 line, plain words."
    )
    return generate_response(prompt, max_length=60)


# ---------------- Policy Summarization ----------------
def policy_summarization(pdf_file, policy_text):
    if pdf_file:
        content = extract_text_from_pdf(pdf_file)
        if content.startswith("Error"):
            return content
        summary_prompt = (
            "Summarize this policy in 3-4 plain sentences. "
            "Keep it very short, clear, and simple:\n\n" + content
        )
    elif policy_text:
        summary_prompt = (
            "Summarize this policy in 3-4 plain sentences. "
            "Keep it very short, clear, and simple:\n\n" + policy_text
        )
    else:
        return "Please upload a PDF or paste text."

    return generate_response(summary_prompt, max_length=80)


# ---------------- Gradio UI ----------------
with gr.Blocks() as app:
    gr.Markdown("## 🌿 Eco Assistant & Policy Analyzer 📜")

    with gr.Tabs():
        # Eco Tips Tab
        with gr.Tab("Eco Tips Generator"):
            keywords_input = gr.Textbox(
                label="Environmental Keywords",
                placeholder="e.g., plastic, water waste, solar...",
                lines=2
            )
            generate_tips_btn = gr.Button("Generate Tips")
            tips_output = gr.Textbox(
                label="Eco Tips",
                lines=5,
                show_copy_button=True
            )
            generate_tips_btn.click(
                fn=eco_tips_generator,
                inputs=keywords_input,
                outputs=tips_output
            )

        # Policy Summarization Tab
        with gr.Tab("Policy Summarization"):
            pdf_upload = gr.File(
                label="Upload Policy PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            policy_text_input = gr.Textbox(
                label="Or Paste Policy Text",
                placeholder="Paste policy document text...",
                lines=4
            )
            summarize_btn = gr.Button("Summarize Policy")
            summary_output = gr.Textbox(
                label="Policy Summary",
                lines=7,
                show_copy_button=True
            )
            summarize_btn.click(
                fn=policy_summarization,
                inputs=[pdf_upload, policy_text_input],
                outputs=summary_output
            )

# ---------------- Launch ----------------
app.launch(share=True)
