import streamlit as st
from openai import OpenAI
import datetime

client = OpenAI(api_key = st.secrets["OpenAI_key"])


def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ---- APP UI ------
st.title("🧠 Agentic AI Freight Assistant")

st.markdown("""
This prototype uses agentic AI logic to:
- Normalize truck/load input
- Suggest potential matches
- Filter profanity and risky content
""")

entry_type = st.radio("What are you posting?", ["Truck", "Load"])
voice_input = st.text_area("Enter voice-to-text or manual description:",
                            placeholder="e.g., Flatbed truck in Dallas available tomorrow, headed to Denver")

submit = st.button("Analyze with Agent")

if submit and voice_input:
    # ---------------------- PROMPTING AGENTS ----------------------
    st.subheader("📋 Normalized Output")
    normalize_prompt = f"""
    Normalize this freight entry into structured fields: Type, City, State, Availability Date, Destination.
    Example: "Flatbed truck in Dallas available tomorrow, headed to Denver" => 
    Type: Flatbed\nCity: Dallas\nState: TX\nAvailability Date: YYYY-MM-DD\nDestination: Denver, CO\n
    Entry: {voice_input}
    """
    normalized_output = call_llm(normalize_prompt)
    st.code(normalized_output)

    st.subheader("⚠️ Profanity / Risk Check")
    risk_check_prompt = f"Detect if the following text contains profanity or risky broker circumvention phrases. If yes, explain.\n\nText: {voice_input}"
    risk_output = call_llm(risk_check_prompt)
    st.warning(risk_output)

    st.subheader("🔍 Suggested Match (if applicable)")
    match_prompt = f"""
    A truck is posted with the following info:\n{normalized_output}\n
    Are there any load matches from this list:\n1. Lubbock to Denver, flatbed\n2. Tulsa to Amarillo, van\n3. Dallas to Houston, flatbed\n
    Suggest a match and explain why or why not.
    """
    match_output = call_llm(match_prompt)
    st.success(match_output)

    st.caption("Prototype powered by OpenAI GPT-4. Not for production use.")



