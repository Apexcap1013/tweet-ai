import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Growth Engine", page_icon="⚡", layout="centered")

# --- 2. SECURE API KEY HANDLING ---
# This checks if the key is stored in Streamlit Cloud Secrets.
# If not (running locally), it looks for a fallback or environment variable.
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # If running locally on your Mac, you can paste your key here for testing
    # BUT DO NOT UPLOAD THIS KEY TO GITHUB
    api_key = "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING_ONLY"

genai.configure(api_key=api_key)

# --- 3. MODERN MOBILE STYLING (THE FIX) ---
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* CUSTOM CARD STYLE - FORCES BLACK TEXT */
    .tweet-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #007AFF;
    }

    /* FORCE all text inside the card to be black */
    .tweet-card div, .tweet-card p, .tweet-card h3 {
        color: #000000 !important;
    }

    /* Image Card Style */
    .image-card {
        border-radius: 15px;
        overflow: hidden;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Modern Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        background-color: #007AFF;
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: transform 0.1s;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Input Field Styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AI MODEL SETUP ---
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction="""
    You are a high-engagement social media strategist.
    Output Format:
    Tweet: [Text]
    Image Prompt: [Visual Description]
    """
)

# --- 5. THE APP INTERFACE ---

# Header
col1, col2 = st.columns([1, 5])
with col1:
    # Use a generic icon or logo
    st.markdown("🚀")
with col2:
    st.markdown("### **Growth Engine**")

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["🔥 Roast / Reply", "📰 News to Viral"])

# ==========================================
# TAB 1: REPLY MODE
# ==========================================
with tab1:
    # Collapsible Search Menu
    with st.expander("⚙️ Search Trending Topics", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📈 Inflation"):
                st.markdown("[Open X](https://x.com/search?q=inflation&src=typed_query&f=live)", unsafe_allow_html=True)
        with c2:
            if st.button("🤖 AI"):
                st.markdown("[Open X](https://x.com/search?q=Artificial+Intelligence&src=typed_query&f=live)", unsafe_allow_html=True)
        with c3:
            if st.button("🗳️ Politics"):
                st.markdown("[Open X](https://x.com/search?q=Politics&src=typed_query&f=live)", unsafe_allow_html=True)

    # Input Area
    tweet_text = st.text_area("Paste Tweet URL or Text:", height=100, placeholder="Paste the tweet you want to roast here...")
    
    # Tone Selector
    st.write("**Select Tone:**")
    t1, t2, t3 = st.columns(3)
    tone = "Cynical" # Default
    if t1.button("🤡 Clown"): tone = "Mocking/Clown World"
    if t2.button("🧠 Smart"): tone = "Intellectual/Data"
    if t3.button("🔥 Roast"): tone = "Aggressive/Roast"

    # Generate Button
    if st.button("Generate Reply ⚡️"):
        if tweet_text:
            with st.spinner("Analyzing..."):
                try:
                    prompt = f"Write a {tone} reply to: '{tweet_text}'. Keep it under 280 chars. Just the text."
                    response = model.generate_content(prompt)
                    
                    # Display Result in Custom Card (Black Text)
                    st.markdown(f"""
                    <div class="tweet-card">
                        <div style="font-size: 12px; color: #555 !important; margin-bottom: 5px; text-transform: uppercase;">Generated Reply ({tone})</div>
                        <div style="font-size: 16px; font-weight: 500;">{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# TAB 2: NEWS MODE
# ==========================================
with tab2:
    news_content = st.text_area("Paste Article Headline:", height=100, placeholder="E.g. 'New law bans remote work...'")
    
    if st.button("Create Viral Post 🚀"):
        if news_content:
            with st.spinner("Creating content..."):
                try:
                    prompt = f"""
                    Topic: "{news_content}"
                    1. Write a viral tweet (controversial/engaging).
                    2. Describe a dramatic image to go with it.
                    Separate with |||
                    """
                    response = model.generate_content(prompt)
                    
                    # Parse the result
                    parts = response.text.split("|||")
                    tweet = parts[0].replace("Tweet:", "").strip()
                    img_prompt = parts[1].replace("Image Prompt:", "").strip() if len(parts) > 1 else "Abstract news background"
                    
                    # 1. Show Tweet Card (Black Text)
                    st.markdown(f"""
                    <div class="tweet-card">
                        <div style="font-size: 12px; color: #555 !important; margin-bottom: 5px; text-transform: uppercase;">Viral Tweet</div>
                        <div style="font-size: 18px; font-weight: 600;">{tweet}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 2. Show Image
                    clean_prompt = img_prompt.replace(" ", "%20")
                    st.markdown(f"""
                    <div class="image-card">
                        <img src="https://image.pollinations.ai/prompt/{clean_prompt}?nologo=true" style="width:100%">
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("Could not generate content. Please try again.")