from google import genai
import streamlit as st

# Load from secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def eco_bot_response(user_input, latest_data):
    try:
        prompt = f"""
You are an environmental water expert.

Sensor Data:
pH: {latest_data['pH']}
TDS: {latest_data['TDS']}
Turbidity: {latest_data['Turbidity']}

User query: {user_input}

Give:
- contamination type
- cause
- eco-friendly solution
Keep it short (max 5 lines).
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"⚠️ AI ERROR: {str(e)}"