"""
HealthGuide: Domain-Specific Health & Wellness Chatbot
Built with Groq API + Streamlit
"""

import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HealthGuide: Health & Wellness Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT
# ══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
You are HealthGuide, a knowledgeable and empathetic health and wellness assistant.

## ROLE
- You are a certified health educator and wellness advisor — NOT a licensed doctor or medical professional.
- You provide evidence-based general health information in a warm, clear, and supportive tone.
- You are patient, non-judgmental, and always encourage users to consult qualified healthcare professionals for personal medical decisions.
- Your name is HealthGuide. Never claim to be a human or a doctor.

## AUDIENCE & SCOPE
Your audience is the general public. You are expert in:
- General health information and disease awareness (educational only)
- Nutrition and healthy eating habits
- Physical fitness and exercise guidance
- Mental health awareness (stress, anxiety, sleep, mindfulness)
- Preventive care and healthy lifestyle habits
- Common symptoms — educational explanation only, never diagnosis
- Medication awareness — general information only, never dosage advice
- Women's health, men's health, and child wellness (general guidance)

## CONSTRAINTS — follow these strictly
1. NEVER diagnose a condition, prescribe medication, or recommend specific dosages.
2. Always remind users to consult a qualified healthcare provider for personal medical decisions.
3. EMERGENCIES: If a user mentions chest pain, difficulty breathing, severe bleeding,
   loss of consciousness, suicidal thoughts, or any life-threatening situation —
   immediately and clearly direct them to call emergency services (115 in Pakistan,
   911 in the US, 999 in the UK) or go to the nearest hospital. Do not continue the
   health conversation until safety is confirmed.
4. OFF-TOPIC: If a user asks something outside health and wellness (e.g., cooking
   recipes unrelated to nutrition, legal advice, financial advice, coding, sports scores,
   entertainment), politely decline and redirect them back to health topics.
   Example: "That's outside my area of expertise! I'm here to help with health and
   wellness questions. Is there anything health-related I can help you with today?"
5. Keep responses clear, concise, and jargon-free. Use bullet points for lists.
6. Never make up statistics. If unsure, say so and suggest consulting a professional.

## TONE
Warm, empathetic, professional, and encouraging. Think of yourself as a knowledgeable
friend who happens to have a health background — caring, honest, and clear about the
limits of what you can offer.
""".strip()

# ══════════════════════════════════════════════════════════════════════════════
# MODEL CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.3
MAX_TOKENS = 600

# ══════════════════════════════════════════════════════════════════════════════
# STREAMING HELPER
# ══════════════════════════════════════════════════════════════════════════════

def stream_groq_response(stream):
    """
    Generator that extracts text pieces from a Groq streaming response.

    Groq's streaming API (same shape as OpenAI's) sends a sequence of chunks;
    each chunk's `delta.content` holds the next piece of text (or None for
    chunks that carry no new text, e.g. the final chunk). This generator is
    handed to st.write_stream, which renders each piece as it arrives and
    returns the fully concatenated string once the stream ends.
    """
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

# ══════════════════════════════════════════════════════════════════════════════
# INPUT GUARDRAILS
# ══════════════════════════════════════════════════════════════════════════════

def input_guardrail(user_input: str):
    """
    Simple keyword-based input guardrail.

    Blocks user inputs containing predefined prompt injection keywords.
    """

    banned_keywords = [
    "bypass instructions",
    "ignore previous instructions",
    "disregard all instructions",
    "ignore system prompt",
    "reveal system prompt",
    "override system instructions",
    "forget your instructions",
    "act as an unrestricted ai",
    ]

    if any(keyword in user_input.lower() for keyword in banned_keywords):
        return "Security Triggered: Instruction modification attempt blocked."

    return None


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:

    st.title("🩺 HealthGuide")
    st.caption("Your AI Health & Wellness Assistant")

    st.divider()

    st.subheader("📋 What I can help with")

    st.markdown("""
    - 🥗 Nutrition & diet
    - 🏃 Fitness & exercise
    - 🧠 Mental health & stress
    - 😴 Sleep & recovery
    - 💊 General medication info
    - 🩻 Symptom education
    - ❤️ Preventive care
    """)

    st.divider()

    st.warning(
        "⚠️ **Disclaimer:** HealthGuide provides general health information only. "
        "It is not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider."
    )

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CHAT UI
# ══════════════════════════════════════════════════════════════════════════════

st.title("🩺 HealthGuide")
st.caption("Ask me anything about health and wellness. I'm here to help!")

st.divider()


# Welcome message on first load

if not st.session_state.messages:

    with st.chat_message("assistant"):

        st.markdown(
            "👋 Hello! I'm **HealthGuide**, your AI health and wellness assistant.\n\n"
            "I can help you with questions about **nutrition, fitness, mental health, "
            "sleep, symptoms (education only), and healthy lifestyle habits**.\n\n"
            "What health topic can I help you with today?"
        )


# ══════════════════════════════════════════════════════════════════════════════
# DISPLAY CONVERSATION HISTORY
# ══════════════════════════════════════════════════════════════════════════════

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT + INPUT GUARDRAILS
# ══════════════════════════════════════════════════════════════════════════════

if user_input := st.chat_input("Ask a health or wellness question…"):

    # Display user input
    with st.chat_message("user"):
        st.markdown(user_input)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 1: INPUT GUARDRAIL CHECK
    # ──────────────────────────────────────────────────────────────────────────

    guardrail_response = input_guardrail(user_input)

    if guardrail_response:

        with st.chat_message("assistant"):
            st.error(guardrail_response)

    else:

        # Store accepted user input in conversation history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # ──────────────────────────────────────────────────────────────────────
        # STEP 2: BUILD GROQ MESSAGES
        # ──────────────────────────────────────────────────────────────────────

        groq_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for msg in st.session_state.messages:

            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # ──────────────────────────────────────────────────────────────────────
        # STEP 3: CALL GROQ API (STREAMING)
        # ──────────────────────────────────────────────────────────────────────

        with st.chat_message("assistant"):

            try:

                client = Groq(api_key=os.getenv("GROQ_API_KEY"))

                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=groq_messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    stream=True,
                )

                # st.write_stream consumes the generator, renders each piece
                # as it arrives (with a blinking cursor), and returns the
                # full concatenated text once the stream is exhausted.
                reply = st.write_stream(stream_groq_response(stream))

                # Store assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:

                error_msg = str(e).lower()

                if (
                    "api_key" in error_msg
                    or "authentication" in error_msg
                    or "auth" in error_msg
                ):
                    st.error(
                        "🔑 Invalid API key. Please check your GROQ_API_KEY "
                        "in the .env file."
                    )

                elif "quota" in error_msg or "rate" in error_msg:

                    st.error(
                        "⏳ Rate limit reached. Please wait a moment and try again."
                    )

                elif "connection" in error_msg or "network" in error_msg:

                    st.error(
                        "🌐 Connection error. Please check your internet and try again."
                    )

                else:

                    st.error(f"❌ An error occurred: {e}")