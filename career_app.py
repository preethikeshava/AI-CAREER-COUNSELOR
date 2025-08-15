import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# --- Page Config ---
st.set_page_config(
    page_title="Career Navigator",
    page_icon="🚀",
    layout="wide"
)

# --- Lottie Animation Loader ---
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_career = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# --- CSS Styling for Top Navbar ---
st.markdown("""
    <style>
    /* Top Navbar Styling */
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #1f1f1f;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .navbar a {
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .navbar a:hover {
        background-color: #ff6ec4;
        border-radius: 8px;
    }
    .active {
        background-color: #7873f5;
        border-radius: 8px;
    }
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
        color: white;
    }
    .title {
        font-size: 2.2rem;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #ff6ec4, #7873f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Top Navbar Links ---
pages = ["🏠 Home", "🧠 Career Predictor", "💼 Job Finder"]
selected_page = st.session_state.get("selected_page", "🏠 Home")

# Navbar HTML
nav_links = ""
for page in pages:
    if page == selected_page:
        nav_links += f'<a class="active">{page}</a>'
    else:
        nav_links += f'<a href="?page={page}">{page}</a>'
st.markdown(f'<div class="navbar">{nav_links}</div>', unsafe_allow_html=True)

# Get URL params to switch pages
query_params = st.experimental_get_query_params()
if "page" in query_params:
    selected_page = query_params["page"][0]
    st.session_state["selected_page"] = selected_page

# --- HOME PAGE ---
if selected_page == "🏠 Home":
    st.markdown('<p class="title">🚀 Welcome to Career Navigator</p>', unsafe_allow_html=True)
    st.write("Your AI-powered tool to discover the right career path and find real-time job openings.")
    st_lottie(lottie_career, height=300)
    st.success("Tip: Use the top navigation bar to explore different sections!")

# --- CAREER PREDICTOR ---
elif selected_page == "🧠 Career Predictor":
    st.markdown('<p class="title">🧠 AI Career Predictor</p>', unsafe_allow_html=True)
    math_score = st.slider("📊 Math Score", 0, 100, 50)
    coding_skill = st.slider("💻 Coding Skill", 0, 100, 50)
    interest_ai = st.checkbox("🤖 Interested in AI?")
    interest_cloud = st.checkbox("☁ Interested in Cloud Computing?")

    if st.button("Predict Career 🚀"):
        with st.spinner("Analyzing your skills..."):
            import time
            time.sleep(1)
        st.success("You are best suited for: **Data Scientist**")
        st.balloons()

# --- JOB FINDER ---
elif selected_page == "💼 Job Finder":
    st.markdown('<p class="title">💼 Real-Time Job Finder</p>', unsafe_allow_html=True)
    response = requests.get("https://arbeitnow.com/api/job-board-api")
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        for job in jobs[:5]:
            st.markdown(f"""
                <div class="glass-card">
                    <h3>{job['title']}</h3>
                    <p>🏢 {job['company_name']} | 📍 {job['location']}</p>
                    <a href="{job['url']}" target="_blank">🔗 Apply Here</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ Unable to fetch jobs at the moment.")
