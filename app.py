import streamlit as st
import google.generativeai as genai

# 1. Setup Gemini API
# Yahan apni API Key dalein ya Streamlit secrets use karein
API_KEY = "AIzaSyDiIKEpN6uMB41BqdfK7RIzkX-YpbbbEFE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Configuration
st.set_page_config(page_title="FirstResponse.Ai", page_icon="🚑")

st.markdown("# 🚑 FirstResponse.Ai")
st.info("Emergency First-Aid Assistant: Doctor ke anay tak kya karna hai?")

# 3. System Prompt (The Rules)
SYSTEM_PROMPT = """
You are an expert Emergency Medical Responder. Your goal is to provide life-saving first-aid 
instructions to someone in a crisis. 
Rules:
1. ALWAYS start by telling the user to call 1122, 911, or local emergency services.
2. Give short, bulleted, step-by-step instructions.
3. Be calm, clear, and direct.
4. If it's a life-threatening situation (like no breathing), prioritize CPR or bleeding control.
5. Use simple English or Urdu if requested.
"""

# 4. User Interaction
user_query = st.text_input("Kya emergency pesh ayi hai? (Maslan: Choking, Heart Attack, Deep Cut)")

if user_query:
    with st.spinner('Generating life-saving instructions...'):
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Emergency: {user_query}"
            response = model.generate_content(full_prompt)
            
            st.markdown("### 📝 Fori Iqdaamat (Immediate Steps):")
            st.write(response.text)
            
            st.warning("Disclaimer: Yeh AI mashwara hai. Asal doctor ki jagah nahi le sakta.")
        except Exception as e:
            st.error(f"Error: {e}")

# 5. Sidebar info
st.sidebar.title("About")
st.sidebar.write("FirstResponse.Ai helps bridge the gap during the 'Golden Hour' of medical emergencies.")