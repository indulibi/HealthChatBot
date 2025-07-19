# 🤖 HealthBot  

HealthBot is a simple **AI health chatbot** made with Python, Google Gemini API, and Tkinter GUI.  

---

## ✨ What it does  
✅ You type symptoms like *fever and headache*  
✅ It gives basic health tips  
✅ Shows “Thinking…” while AI responds  
✅ Has a GUI with Send, Clear Chat, Quit buttons  
✅ Remembers old chat history  

---

## 🖥️ How to Run  

1️⃣ **Install required libraries**  
```bash
pip install google-generativeai tk
2️⃣ Create a config.json file with your own API key

json
Copy code
{
  "GEMINI_API_KEY": "your-own-api-key-here"
}
3️⃣ Run the chatbot

bash
Copy code
python health_chatbot.py