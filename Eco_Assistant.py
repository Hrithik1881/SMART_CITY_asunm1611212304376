import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import base64

# ---------------- Setup Gemini API ----------------
encoded_api = "QUl6YVN5Qmpuc25jSDNoandvUDRlZVlwRm5YWnd3NUpBb0NPbTlV"  # base64
API_KEY = base64.b64decode(encoded_api).decode("utf-8")
MODEL = "gemini-1.5-flash"

def call_gemini(prompt, max_tokens=80):
    """Call Gemini API with a given prompt"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.2
                }
            }
        )
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response.")
    except Exception as e:
        return "Error: " + str(e)


# ---------------- Tkinter UI ----------------
root = tk.Tk()
root.title("🌿 Eco Assistant & Policy Analyzer 📜")
root.geometry("720x520")
root.configure(bg="#f4f9f4")

# ---------------- Header ----------------
header = tk.Label(
    root, text="🌿 Eco Assistant & Policy Analyzer 📜",
    bg="#4CAF50", fg="white",
    font=("Arial", 18, "bold"), pady=12
)
header.pack(fill="x")

# ---------------- Tabs ----------------
tab_frame = tk.Frame(root, bg="#e8f5e9")
tab_frame.pack(fill="x")

current_tab = tk.StringVar(value="eco")

def switch_tab(tab_name):
    current_tab.set(tab_name)
    if tab_name == "eco":
        eco_frame.pack(fill="both", expand=True)
        policy_frame.forget()
        btn_eco.config(bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        btn_policy.config(bg="#e8f5e9", fg="black", font=("Arial", 11))
    else:
        policy_frame.pack(fill="both", expand=True)
        eco_frame.forget()
        btn_policy.config(bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        btn_eco.config(bg="#e8f5e9", fg="black", font=("Arial", 11))

btn_eco = tk.Button(tab_frame, text="Eco Tips Generator",
                    relief="flat", bd=0, padx=10, pady=8,
                    bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                    command=lambda: switch_tab("eco"))
btn_eco.pack(side="left", expand=True, fill="x")

btn_policy = tk.Button(tab_frame, text="Policy Summarization",
                       relief="flat", bd=0, padx=10, pady=8,
                       bg="#e8f5e9", fg="black", font=("Arial", 11),
                       command=lambda: switch_tab("policy"))
btn_policy.pack(side="left", expand=True, fill="x")

# ---------------- Eco Tips Frame ----------------
eco_frame = tk.Frame(root, bg="#f4f9f4")
eco_frame.pack(fill="both", expand=True)

tk.Label(eco_frame, text="Environmental Keywords:", bg="#f4f9f4",
         font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=8)
eco_keywords = tk.Entry(eco_frame, font=("Arial", 11), relief="solid", bd=1)
eco_keywords.pack(padx=15, pady=5, fill="x")

eco_output = scrolledtext.ScrolledText(
    eco_frame, wrap=tk.WORD, height=12,
    font=("Arial", 11), relief="solid", bd=1
)
eco_output.pack(padx=15, pady=10, fill="both", expand=True)

def generate_eco_tips():
    text = eco_keywords.get().strip()
    if not text:
        messagebox.showwarning("Input needed", "Please enter some keywords.")
        return
    eco_output.delete("1.0", tk.END)
    eco_output.insert(tk.END, "🌱 Generating tips...\n")
    prompt = f"Give 3 very short eco-friendly tips about {text}. Each tip must be max 1 line, plain words."
    result = call_gemini(prompt, max_tokens=60)
    eco_output.delete("1.0", tk.END)
    eco_output.insert(tk.END, result)

tk.Button(eco_frame, text="Generate Tips",
          bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
          relief="flat", padx=12, pady=6,
          command=generate_eco_tips).pack(pady=6)

# ---------------- Policy Frame ----------------
policy_frame = tk.Frame(root, bg="#f4f9f4")

tk.Label(policy_frame, text="Paste Policy Text:", bg="#f4f9f4",
         font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=8)

policy_text = scrolledtext.ScrolledText(
    policy_frame, wrap=tk.WORD, height=8,
    font=("Arial", 11), relief="solid", bd=1
)
policy_text.pack(padx=15, pady=5, fill="both", expand=False)

policy_output = scrolledtext.ScrolledText(
    policy_frame, wrap=tk.WORD, height=10,
    font=("Arial", 11), relief="solid", bd=1
)
policy_output.pack(padx=15, pady=10, fill="both", expand=True)

def summarize_policy():
    text = policy_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input needed", "Please paste some policy text.")
        return
    policy_output.delete("1.0", tk.END)
    policy_output.insert(tk.END, "📜 Summarizing...\n")
    prompt = f"Summarize this policy in 3-4 plain sentences. Keep it very short, clear, and simple:\n\n{text}"
    result = call_gemini(prompt, max_tokens=80)
    policy_output.delete("1.0", tk.END)
    policy_output.insert(tk.END, result)

tk.Button(policy_frame, text="Summarize Policy",
          bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
          relief="flat", padx=12, pady=6,
          command=summarize_policy).pack(pady=6)

# ---------------- Start App ----------------
root.mainloop()
