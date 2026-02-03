import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION & MODERN STYLING ---
# Load API Key securely from Streamlit Cloud
import os
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Fallback for local testing if you have a .env file or just manually paste it for now
    api_key = "PASTE_YOUR_KEY_HERE_FOR_LOCAL_ONLY" 

st.set_page_config(page_title="TweetAI", page_icon="⚡", layout="centered")

# This CSS block creates the "Native App" look
st.markdown("""
    <style>
    /* 1. Import a modern font (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 2. Hide Streamlit Branding (Hamburger menu, footer, colored bar) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* 3. Style the "Cards" (Result boxes) */
    .stSuccess {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 20px;
        color: #1a1a1a;
    }

    /* 4. Make Buttons look like "App" buttons (Full width, rounded) */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        background-color: #007AFF; /* iOS Blue */
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        transform: scale(1.02);
    }

    /* 5. Custom "Card" container for generated text */
    .tweet-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border-left: 5px solid #007AFF;
    }
    
    .image-card {
        border-radius: 15px;
        overflow: hidden;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* 6. Clean up text inputs */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction="""
    You are a high-engagement social media strategist.
    Output Format:
    Tweet: [Text]
    Image Prompt: [Visual Description]
    """
)

# --- HEADER (Looks like a mobile nav bar) ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg", width=40)
with col2:
    st.markdown("### **Growth Engine**")

st.markdown("---")

# --- MOBILE TABS ---
tab1, tab2 = st.tabs(["🔥 Roast / Reply", "📰 News to Viral"])

# ==========================================
# TAB 1: REPLY MODE
# ==========================================
with tab1:
    # Use an "Expander" to hide the settings on mobile to save space
    with st.expander("⚙️ Search & Settings", expanded=False):
        st.caption("Quick Find Trending Topics:")
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

    tweet_text = st.text_area("Paste Tweet URL or Text:", height=100, placeholder="Paste the controversial tweet here...")
    
    # Tone Selector (Pill style using columns)
    st.write("**Select Tone:**")
    t1, t2, t3 = st.columns(3)
    tone = "Cynical" # Default
    if t1.button("🤡 Clown"): tone = "Mocking/Clown World"
    if t2.button("🧠 Smart"): tone = "Intellectual/Data"
    if t3.button("🔥 Roast"): tone = "Aggressive/Roast"

    if st.button("Generate Reply ⚡️"):
        if tweet_text:
            with st.spinner("Analyzing..."):
                prompt = f"Write a {tone} reply to: '{tweet_text}'. Keep it under 280 chars."
                response = model.generate_content(prompt)
                
                # Render the custom HTML card
                st.markdown(f"""
                <div class="tweet-card">
                    <div style="font-size: 12px; color: #888; margin-bottom: 5px;">GENERATED REPLY ({tone.upper()})</div>
                    <div style="font-size: 16px; font-weight: 500;">{response.text}</div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: NEWS MODE
# ==========================================
with tab2:
    news_content = st.text_area("Paste Article Headline:", height=100, placeholder="E.g. 'New law bans remote work...'")
    
    if st.button("Create Viral Post 🚀"):
        if news_content:
            with st.spinner("Creating content..."):
                prompt = f"""
                Topic: "{news_content}"
                1. Write a viral tweet (controversial/engaging).
                2. Describe a dramatic image to go with it.
                Separate with |||
                """
                response = model.generate_content(prompt)
                
                try:
                    parts = response.text.split("|||")
                    tweet = parts[0].replace("Tweet:", "").strip()
                    img_prompt = parts[1].replace("Image Prompt:", "").strip() if len(parts) > 1 else "Abstract news background"
                    
                    # 1. Show Tweet Card
                    st.markdown(f"""
                    <div class="tweet-card">
                        <div style="font-size: 12px; color: #888; margin-bottom: 5px;">VIRAL TWEET</div>
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
                    
                except:
                    st.error("Could not parse response. Try again.")
