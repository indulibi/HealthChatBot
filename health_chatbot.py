import google.generativeai as genai
import json
import tkinter as tk
from tkinter import scrolledtext, font
import os

# ✅ Load API key securely from config.json
with open("config.json") as f:
    key_data = json.load(f)

genai.configure(api_key=key_data["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def get_health_response(symptoms):
    """Generate AI health advice"""
    prompt = f"I have these symptoms: {symptoms}. Give short, clear health tips and tell if I should see a doctor."
    response = model.generate_content(prompt)
    return response.text

def save_history(user_input, bot_reply):
    """Save chat to history file"""
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\nHealthBot: {bot_reply}\n\n")

def load_previous_history():
    """Load old chat history if exists"""
    if os.path.exists("chat_history.txt"):
        with open("chat_history.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "🤖 HealthBot: Hello! I can give basic health tips. Type 'quit' to stop.\n\n"

def send_message(event=None):
    symptoms = entry.get().strip()
    if not symptoms:
        return

    # Show user message
    chat_area.insert(tk.END, f"You: {symptoms}\n", "user")
    chat_area.insert(tk.END, "🤖 HealthBot: Thinking...\n", "thinking")
    chat_area.yview(tk.END)
    entry.delete(0, tk.END)

    if symptoms.lower() == "quit":
        chat_area.insert(tk.END, "🤖 HealthBot: Take care! Goodbye!\n", "bot")
        root.after(2000, root.destroy)
        return

    # Get AI advice
    advice = get_health_response(symptoms)
    advice += "\n💡 Self-care Tip: Drink plenty of water and rest well."

    # Remove "Thinking..." and show final answer
    chat_area.delete("end-3l", "end-2l")
    chat_area.insert(tk.END, f"🤖 HealthBot: {advice}\n\n", "bot")
    chat_area.yview(tk.END)

    save_history(symptoms, advice)

def clear_chat():
    """Clear the chat screen"""
    chat_area.delete(1.0, tk.END)

# ✅ GUI Window Setup
root = tk.Tk()
root.title("HealthBot (Gemini)")
root.geometry("750x550")
root.configure(bg="#e6f2ff")  # Light blue background

# ✅ Fonts
chat_font = font.Font(family="Segoe UI", size=11)

# ✅ Chat Display Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25,
                                      font=chat_font, bg="#ffffff", fg="#000000")
chat_area.pack(padx=10, pady=10)

# ✅ Load previous chat history
previous_history = load_previous_history()
chat_area.insert(tk.END, previous_history, "bot")

# ✅ Colored Text Styles
chat_area.tag_config("user", foreground="blue", font=("Segoe UI", 10, "bold"))
chat_area.tag_config("bot", foreground="green", font=("Segoe UI", 10))
chat_area.tag_config("thinking", foreground="gray", font=("Segoe UI", 9, "italic"))

# ✅ Input + Buttons Frame
entry_frame = tk.Frame(root, bg="#e6f2ff")
entry_frame.pack(pady=8)

entry = tk.Entry(entry_frame, width=50, font=chat_font)
entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(entry_frame, text="Send", command=send_message,
                        bg="#4CAF50", fg="white", width=10)
send_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(entry_frame, text="Clear Chat", command=clear_chat,
                         bg="#ff9800", fg="white", width=12)
clear_button.grid(row=0, column=2, padx=5)

quit_button = tk.Button(entry_frame, text="Quit", command=root.destroy,
                        bg="#f44336", fg="white", width=10)
quit_button.grid(row=0, column=3, padx=5)

# ✅ Press Enter to Send
root.bind('<Return>', send_message)

root.mainloop()
