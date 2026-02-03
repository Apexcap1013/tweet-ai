import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Growth Engine", page_icon="⚡", layout="centered")

# --- 2. SECURE API KEY HANDLING ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING_ONLY"

genai.configure(api_key=api_key)

# --- 3. MODERN MOBILE STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* CARD STYLING */
    .tweet-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #007AFF;
    }

    /* Force black text */
    .tweet-card div, .tweet-card p, .tweet-card h3 {
        color: #000000 !important;
    }

    /* Image Card */
    .image-card {
        border-radius: 15px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        background-color: #007AFF;
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AI MODEL SETUP ---
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction="""
    You are a viral social media strategist.
    Always provide 3 distinct options.
    For News Mode, provide a distinct Image Prompt for each option.
    Separate options with "|||"
    """
)

# --- 5. THE APP INTERFACE ---

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🚀")
with col2:
    st.markdown("### **Growth Engine**")

st.markdown("---")

tab1, tab2 = st.tabs(["🔥 Roast / Reply", "📰 News to Viral"])

# ==========================================
# TAB 1: REPLY MODE (3 Options + Custom Input)
# ==========================================
with tab1:
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

    tweet_text = st.text_area("Paste Tweet URL or Text:", height=100, placeholder="Paste tweet here...")
    
    # NEW: Custom Direction Input
    user_direction = st.text_input("My Custom Direction (Optional):", placeholder="e.g. Mention the price of eggs, be sarcastic...")

    st.write("**Select Tone:**")
    t1, t2, t3 = st.columns(3)
    tone = "Cynical" 
    if t1.button("🤡 Clown"): tone = "Mocking/Clown World"
    if t2.button("🧠 Smart"): tone = "Intellectual/Data"
    if t3.button("🔥 Roast"): tone = "Aggressive/Roast"

    if st.button("Generate 3 Replies ⚡️"):
        if tweet_text:
            with st.spinner("Cooking up 3 options..."):
                try:
                    # Construct prompt with user direction
                    direction_text = f"Specific instruction: {user_direction}." if user_direction else ""
                    prompt = f"Write 3 distinct {tone} replies to: '{tweet_text}'. {direction_text} Keep under 280 chars. Separate each reply with |||"
                    
                    response = model.generate_content(prompt)
                    options = response.text.split("|||")
                    
                    for i, option in enumerate(options):
                        if option.strip():
                            st.markdown(f"""
                            <div class="tweet-card">
                                <div style="font-size: 12px; color: #555 !important; margin-bottom: 5px; text-transform: uppercase;">OPTION {i+1}</div>
                                <div style="font-size: 16px; font-weight: 500;">{option.strip()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# TAB 2: NEWS MODE (3 Options + Custom Input)
# ==========================================
with tab2:
    news_content = st.text_area("Paste Article Headline:", height=100, placeholder="E.g. 'New law bans remote work...'")
    
    # NEW: Custom Direction Input
    news_direction = st.text_input("Angle / Focus (Optional):", placeholder="e.g. Focus on freedom, or make it funny...")
    
    if st.button("Generate 3 Viral Posts 🚀"):
        if news_content:
            with st.spinner("Generating 3 viral angles..."):
                try:
                    direction_text = f"Specific instruction: {news_direction}." if news_direction else ""
                    
                    prompt = f"""
                    Topic: "{news_content}"
                    {direction_text}
                    Generate 3 distinct viral tweets with matching image prompts.
                    Format exactly like this for each option:
                    Tweet: [Text]
                    Image Prompt: [Visual Description]
                    |||
                    """
                    response = model.generate_content(prompt)
                    
                    options = response.text.split("|||")
                    
                    for i, option in enumerate(options):
                        if "Tweet:" in option:
                            lines = option.strip().split("\n")
                            tweet_text = ""
                            img_prompt = "News abstract"
                            
                            for line in lines:
                                if "Tweet:" in line:
                                    tweet_text = line.replace("Tweet:", "").strip()
                                if "Image Prompt:" in line:
                                    img_prompt = line.replace("Image Prompt:", "").strip()
                            
                            if tweet_text:
                                st.markdown(f"""
                                <div class="tweet-card">
                                    <div style="font-size: 12px; color: #555 !important; margin-bottom: 5px; text-transform: uppercase;">OPTION {i+1}</div>
                                    <div style="font-size: 18px; font-weight: 600;">{tweet_text}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                clean_prompt = img_prompt.replace(" ", "%20")
                                st.markdown(f"""
                                <div class="image-card">
                                    <img src="https://image.pollinations.ai/prompt/{clean_prompt}?nologo=true" style="width:100%">
                                </div>
                                """, unsafe_allow_html=True)
                                
                except Exception as e:
                    st.error("Could not generate content. Please try again.")