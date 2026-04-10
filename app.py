import streamlit as st
import google.generativeai as genai

# --- VIP UI Configuration ---
st.set_page_config(
    page_title="FirstResponse.Ai | Emergency Agent",
    page_icon="🚑",
    layout="wide"
)

# --- Theme & CSS Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #D32F2F;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #B71C1C;
        color: white;
        transform: scale(1.02);
    }
    .emergency-card {
        padding: 25px;
        border-radius: 15px;
        background-color: #ffffff;
        border-left: 8px solid #D32F2F;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
        color: #212121;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Gemini API Setup ---
# Ensure "GEMINI_API_KEY" is set in your Streamlit Cloud Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key not found. Please configure Secrets in Streamlit Cloud.")

# --- Header Section ---
col1, col2 = st.columns([1, 5])
with col1:
    # Medical Icon
    st.image("https://cdn-icons-png.flaticon.com/512/883/883407.png", width=100)
with col2:
    st.markdown("# **FirstResponse.Ai**")
    st.markdown("### *Your Intelligent First-Aid Companion*")

st.divider()

# --- VIP Options (Quick Response Buttons) ---
st.subheader("🚨 Quick Selection: Choose an Emergency")
st.write("Click a button for instant instructions or describe the situation below:")

c1, c2, c3, c4 = st.columns(4)
quick_query = ""

if c1.button("🩸 Severe Bleeding"):
    quick_query = "Heavy bleeding from a deep wound"
if c2.button("🫁 Choking / Difficulty Breathing"):
    quick_query = "Person is choking and cannot breathe"
if c3.button("⚡ Cardiac Arrest / Unconscious"):
    quick_query = "Person is unconscious and not breathing"
if c4.button("🔥 Severe Burns"):
    quick_query = "Serious burn injury from fire or chemicals"

# --- Search Bar ---
st.markdown("---")
user_input = st.text_input("💬 Describe the emergency in detail:", value=quick_query, placeholder="e.g., Someone fell from stairs and hit their head...")

# --- Logic & AI Response ---
if user_input:
    with st.spinner('Fetching life-saving protocols...'):
        system_prompt = """
        You are a Professional Emergency Medical Responder.
        Structure your response as follows:
        1. MANDATORY: Start with a Bold Red Header: 'STEP 0: CALL EMERGENCY SERVICES IMMEDIATELY!'
        2. 'Immediate Actions': Provide 4-5 high-priority, bulleted, numbered steps. Use bold text for key movements.
        3. 'What NOT to do': List 2-3 critical mistakes to avoid.
        4. 'Observation': What to monitor while waiting for the ambulance.
        Keep it extremely concise and easy to read under pressure.
        """
        try:
            response = model.generate_content(f"{system_prompt}\n\nSituation: {user_input}")
            
            # Displaying in a VIP card
            st.markdown(f"""
                <div class="emergency-card">
                    <h2 style="color: #D32F2F; margin-top:0;">📝 Critical Response Plan</h2>
                    <hr>
                    {response.text}
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error("System timeout. Please try again or check your internet connection.")

# --- Bottom Sidebar ---
st.sidebar.title("🚑 About FirstResponse")
st.sidebar.info("This AI agent provides immediate first-aid guidance during the 'Golden Hour'—the critical period before professional medical help arrives.")
st.sidebar.warning("**Disclaimer:** This is an AI-generated guide for educational/emergency support. Always prioritize professional medical services.")

if st.sidebar.button("🔄 Reset App"):
    st.rerun()
