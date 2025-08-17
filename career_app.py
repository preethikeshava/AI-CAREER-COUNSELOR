import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from PyPDF2 import PdfReader
import re
import joblib
import os
from sklearn.tree import DecisionTreeClassifier
from bs4 import BeautifulSoup

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="Career Navigator", page_icon="🚀", layout="wide")

# ----------------------
# Load Lottie Animation
# ----------------------
@st.cache_data
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_career = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# ----------------------
# File paths
# ----------------------
DATASET_FILE = "job_skills_dataset.xlsx"
MODEL_FILE = "career_model.pkl"

# ----------------------
# Train Model if not exists
# ----------------------
if not os.path.exists(MODEL_FILE):
    df = pd.read_excel(DATASET_FILE)

    # 🔥 Clean column names (remove spaces, unify names)

    df.columns = df.columns.str.strip()          # remove leading/trailing spaces
    df.columns = df.columns.str.replace(r"\s+", "_", regex=True)  # replace spaces with underscores
    df.columns = df.columns.str.replace(r"[^\w]", "_", regex=True)  # replace weird symbols with underscores
    print("Cleaned Columns:", df.columns.tolist())


    # ✅ Now select features
    X = df[["Linguistic","Musical","Bodily","Logical___Mathematical","Spatial_Visualization","Interpersonal",
    "Intrapersonal","Naturalist"]]
    y = df['Job_profession']


    model = DecisionTreeClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)

# Load trained model
career_model = joblib.load(MODEL_FILE)

# ----------------------
# Job Fetching (scraping from Indeed)
# ----------------------
# Fallback: LinkedIn public search
def linkedin_fallback(query):
    query_clean = query.replace("_", " ")
    return [{
        "title": f"Search {query_clean} jobs on LinkedIn",
        "company": "-",
        "location": "-",
        "url": f"https://www.linkedin.com/jobs/search/?keywords={query_clean.replace(' ', '%20')}"
    }]

# Primary: Indeed scraping
def indeed_jobs(query):
    query = query.replace("_", " ")
    jobs = []
    url = f"https://in.indeed.com/jobs?q={query.replace(' ', '+')}&l="
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for card in soup.select(".job_seen_beacon, .tapItem")[:5]:
            title_tag = card.select_one("h2.jobTitle")
            company_tag = card.select_one(".companyName")
            location_tag = card.select_one(".companyLocation")
            link_tag = card.find("a", href=True)

            if title_tag and link_tag:
                jobs.append({
                    "title": title_tag.get_text(strip=True),
                    "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                    "location": location_tag.get_text(strip=True) if location_tag else "N/A",
                    "url": "https://in.indeed.com" + link_tag["href"]
                })
    return jobs

# Master function with fallback
def get_all_jobs(query):
    jobs = indeed_jobs(query)
    if not jobs:  # fallback
        jobs = linkedin_fallback(query)
    return jobs
# ----------------------
# Extract Skills from Resume
# ----------------------
def extract_skills_from_resume(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text().lower() + " "
    skills = re.findall(r"(python|java|cloud|aws|azure|machine learning|ai|javascript|html|css|react)", text)
    return list(set(skills))

# ----------------------
# CSS Styling
# ----------------------
st.markdown("""
    <style>
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
    .navbar a:hover { background-color: #ff6ec4; border-radius: 8px; }
    .active { background-color: #7873f5; border-radius: 8px; }
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

# ----------------------
# Navbar
# ----------------------
pages = ["🏠 Home", "🧠 Career Predictor", "📄 Resume Job Matcher"]
selected_page = st.session_state.get("selected_page", "🏠 Home")

nav_links = ""
for page in pages:
    if page == selected_page:
        nav_links += f'<a class="active">{page}</a>'
    else:
        nav_links += f'<a href="?page={page}">{page}</a>'
st.markdown(f'<div class="navbar">{nav_links}</div>', unsafe_allow_html=True)

query_params = st.experimental_get_query_params()
if "page" in query_params:
    selected_page = query_params["page"][0]
    st.session_state["selected_page"] = selected_page

# ----------------------
# Pages
# ----------------------
if selected_page == "🏠 Home":
    st.markdown('<p class="title">🚀 Welcome to Career Navigator</p>', unsafe_allow_html=True)
    st.write("Discover careers & find jobs instantly.")
    st_lottie(lottie_career, height=300)

elif selected_page == "🧠 Career Predictor":
    st.markdown('<h1 style="text-align:center;">🧠 AI Career Predictor</h1>', unsafe_allow_html=True)

    # ✅ Sliders matching dataset
    lingui = st.slider("🗣 Linguistic Skill", 0, 20, 10)
    music = st.slider("🎵 Musical Skill", 0, 20, 10)
    bodily = st.slider("🏃 Bodily-Kinesthetic", 0, 20, 10)
    logic = st.slider("🧩 Logical Skill", 0, 20, 10)
    spatia = st.slider("📐 Spatial Skill", 0, 20, 10)
    interp = st.slider("🤝 Interpersonal Skill", 0, 20, 10)
    intrap = st.slider("🧘 Intrapersonal Skill", 0, 20, 10)
    natur = st.slider("🌱 Naturalistic Skill", 0, 20, 10)

    if st.button("Predict Career 🚀"):
        input_data = [[lingui, music, bodily, logic, spatia, interp, intrap, natur]]
        prediction = career_model.predict(input_data)[0]

        st.success(f"You are best suited for: **{prediction}**")

        st.subheader("💼 Current Job Offers")
        jobs = get_all_jobs(prediction)
        if jobs:
            for job in jobs:
                st.markdown(f"""
                    <div style="background:#f9f9f9; padding:10px; border-radius:8px; margin-bottom:10px;">
                        <h4>{job['title']}</h4>
                        <p>🏢 {job['company']} | 📍 {job['location']}</p>
                        <a href="{job['url']}" target="_blank">🔗 Apply Here</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching live job postings found right now.")

elif selected_page == "📄 Resume Job Matcher":
    st.markdown('<p class="title">📄 Resume Job Matcher</p>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    if uploaded_resume:
        with st.spinner("Extracting skills..."):
            skills = extract_skills_from_resume(uploaded_resume)
        if skills:
            st.success(f"Skills found: {', '.join(skills)}")
            jobs = []
            for skill in skills:
                jobs.extend(get_all_jobs(skill))
            if jobs:
                st.subheader("🎯 Matching Job Offers")
                for job in jobs[:10]:
                    st.markdown(f"""
                        <div class="glass-card">
                            <h3>{job['title']}</h3>
                            <p>🏢 {job['company']} | 📍 {job['location']}</p>
                            <a href="{job['url']}" target="_blank">🔗 Apply Here</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No matching jobs found.")
        else:
            st.error("No skills detected in the resume.")
