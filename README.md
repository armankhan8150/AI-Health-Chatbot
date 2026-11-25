# HealthGuide: Domain-Specific Health & Wellness Chatbot

A domain-specific AI chatbot that answers health and wellness questions using the **Groq API** and **Streamlit**.

---

## Domain

**Health & Wellness**: covers nutrition, fitness, mental health, sleep, symptom education, preventive care, and healthy lifestyle habits. Politely declines off-topic questions and immediately redirects emergencies to professional services.

---

## System Prompt Design

| Element | Decision |
|---|---|
| **Role** | Health educator and wellness advisor (not a doctor) |
| **Tone** | Warm, empathetic, clear, non-alarmist |
| **Scope** | Nutrition, fitness, mental health, sleep, symptoms (educational only), preventive care |
| **Hard constraints** | No diagnosis, no prescriptions, emergency redirect, off-topic decline |
| **Disclaimer** | Always reminds users to consult a healthcare professional |

### Emergency Handling
If a user mentions chest pain, difficulty breathing, severe bleeding, or suicidal thoughts, the chatbot immediately directs them to emergency services (115 / 911 / 999) and does not continue the health conversation until safety is confirmed.

### Off-Topic Handling
If the user asks about anything outside health and wellness (legal advice, coding, sports, entertainment), the chatbot politely declines and redirects to health topics.

---

## Model Configuration

| Parameter | Value | Justification |
|---|---|---|
| **Model** | `openai/gpt-oss-20b` | Uses Groq-hosted open-weight model inference for health and wellness Q&A |
| **Temperature** | `0.3` | Health info must be consistent and factual. Low temperature reduces hallucination risk and prevents the model from making up medical statistics |
| **Max output tokens** | `600` | Enough for a thorough, readable health response without being overwhelming |

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/armankhan8150/AI-Health-Chatbot.git
cd AI-Health-Chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a Groq API key at: https://console.groq.com

### 4. Run
```bash
streamlit run app.py
```

---

## Deploy to Streamlit Cloud (Free Public Link)

1. Push this repo to GitHub
2. Go to https://share.streamlit.io
3. Click **"New app"** → select your repo → set `app.py` as the main file
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Deploy** → get your public link 🎉

---

## Features

- 🩺 **Domain-focused**: stays strictly within health & wellness
- 🚨 **Emergency detection**: immediately directs to emergency services (115/911/999)
- 🚫 **Off-topic handling**: politely declines and redirects
- 💬 **Conversation history**: remembers context across the full session
- ⚠️ **Graceful error handling**: handles rate limits, auth errors, and connection failures
- 🗑️ **Clear chat button**: reset the conversation at any time
- 🔑 **Secure API key**: loads `GROQ_API_KEY` from `.env` or the runtime environment

---

## Project Structure

```
AI-Health-Chatbot/
├── app.py               # Main Streamlit chatbot
├── requirements.txt     # Python dependencies
├── .env                 # API key (not committed to git)
├── .gitignore           # Excludes .env from git
└── README.md            # This file
```

---

## Disclaimer

HealthGuide provides general health and wellness information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for personal medical decisions.
