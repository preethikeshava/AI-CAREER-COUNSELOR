<<<<<<< HEAD
import streamlit as st
import pandas as pd
import time
import requests
import fitz  # PyMuPDF for PDF reading

# ------------------------ Sidebar ------------------------
st.sidebar.title("🧑‍🎓 User Info")
name = st.sidebar.text_input("👤 Your Name", "Student")
cgpa = st.sidebar.slider("📊 CGPA", 0.0, 10.0, 8.5)
st.sidebar.markdown("---")
st.sidebar.info("📎 Upload resume or take the quiz below!")

# ------------------------ Title ------------------------
st.title("🎓 AI-Powered Career Guidance Counselor")
st.markdown("---")

# ------------------------ Upload CSV ------------------------
st.subheader("📁 Upload Your Profile CSV (Skills, Interests, etc.)")
uploaded_file = st.file_uploader("📄 Upload your CSV", type="csv")

# ------------------------ Upload Resume ------------------------
st.subheader("📄 Optional: Upload Your Resume (PDF)")
pdf_file = st.file_uploader("📎 Upload your Resume", type="pdf")
if pdf_file is not None:
    with st.spinner("📑 Extracting content from resume..."):
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        st.markdown("### 🧾 Resume Extracted Text")
        st.text_area("Resume Preview", text, height=200)

# ------------------------ Natural Language Input ------------------------
st.subheader("🗣️ Describe your interests or career goals")
user_input = st.text_input("Example: 'I love maths and want to work in AI'")

def extract_info(text):
    interests = []
    career_goals = []

    interest_keywords = ["math", "science", "coding", "design", "writing", "hardware", "cloud"]
    career_keywords = ["AI", "data science", "cloud", "software", "web development", "cybersecurity"]

    for word in interest_keywords:
        if word in text.lower():
            interests.append(word)
    for word in career_keywords:
        if word.lower() in text.lower():
            career_goals.append(word)
    return interests, career_goals

if user_input:
    with st.spinner("🔍 Analyzing your interests..."):
        time.sleep(2)
        interests, goals = extract_info(user_input)
        st.markdown("### 🧠 Detected Interests")
        st.write(interests)
        st.markdown("### 🎯 Career Goals")
        st.write(goals)

        if "ai" in [g.lower() for g in goals] or "data science" in [g.lower() for g in goals]:
            st.success("✅ Explore AI, Data Science, or Machine Learning careers.")
        elif "cloud" in [g.lower() for g in goals]:
            st.success("✅ You might enjoy Cloud Computing or DevOps.")
        elif "web development" in [g.lower() for g in goals]:
            st.success("✅ Consider Web Development or UI/UX Design.")
        elif "cybersecurity" in [g.lower() for g in goals]:
            st.success("✅ Look into Cybersecurity and Ethical Hacking.")
        elif "software" in [g.lower() for g in goals]:
            st.success("✅ Explore Software Engineering or App Development.")
        else:
            st.info("🔍 We'll help you explore various career paths.")
        st.balloons()

# ------------------------ Show Uploaded CSV ------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Your Uploaded Data")
    st.dataframe(df)

# ------------------------ Simple Career Quiz ------------------------
st.subheader("📝 Quick Career Quiz")
q1 = st.radio("Do you enjoy solving logic-based problems?", ["Yes", "No"])
q2 = st.radio("Do you like working with data?", ["Yes", "No"])
q3 = st.radio("Are you interested in building websites or apps?", ["Yes", "No"])

if st.button("📌 Get Career Suggestion from Quiz"):
    if q1 == "Yes" and q2 == "Yes":
        st.success("🎯 Consider Data Science, AI, or Software Engineering")
    elif q3 == "Yes":
        st.success("🎯 Consider Web Development or UI/UX Design")
    else:
        st.info("🎓 Explore Management, Design, or Communication careers")

# ------------------------ Real Job Finder (Arbeitnow API) ------------------------
st.subheader("💼 Find Real Jobs")
role = st.text_input("🔍 Enter Job Role (e.g. Data Scientist, Web Developer)", key="jobrole")
location = st.text_input("📍 Enter Location", "India", key="jobloc")
remote_option = st.selectbox("🏠 Remote Option", ["Any", "Remote Only"], index=0)

if st.button("🔎 Search Jobs"):
    with st.spinner("Fetching job listings..."):
        try:
            api_url = "https://www.arbeitnow.com/api/job-board-api"
            response = requests.get(api_url)
            job_data = response.json()

            filtered_jobs = []
            for job in job_data["data"]:
                if (
                    role.lower() in job["title"].lower()
                    and location.lower() in job["location"].lower()
                    and (remote_option == "Any" or job["remote"])
                ):
                    filtered_jobs.append(job)

            if filtered_jobs:
                for job in filtered_jobs[:10]:
                    st.markdown(f"### 🏢 {job['company_name']}")
                    st.write(f"**Role:** {job['title']}")
                    st.write(f"📍 Location: {job['location']}")
                    st.write(f"🏠 Remote: {'Yes' if job['remote'] else 'No'}")
                    st.write(f"[🔗 Apply Here]({job['url']})")
                    st.markdown("---")
            else:
                st.warning("⚠️ No jobs found. Try another role or location.")
        except Exception as e:
            st.error(f"Error fetching jobs: {e}")

# ------------------------ Footer ------------------------
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("👨‍🎓 Name", name)
col2.metric("📈 CGPA", f"{cgpa}")
=======
import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load dataset
data = pd.read_csv("career_data.csv")
print("Available columns:", data.columns.tolist())
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
print(data.columns.tolist())


# Model
X = data[['math_score', 'coding_skill', 'interest_ai', 'interest_cloud']]
y = data['recommended_career']
model = DecisionTreeClassifier()
model.fit(X, y)

# Streamlit UI
st.title("🎓 AI Career Counselor")
st.write("Answer the questions below to get a career suggestion!")

math_score = st.slider("Your Math Score (0-100)", 0, 100, 75)
coding_skill = st.slider("Your Coding Skill (0-100)", 0, 100, 80)
interest_ai = st.selectbox("Interested in AI?", ["No", "Yes"])
interest_cloud = st.selectbox("Interested in Cloud Computing?", ["No", "Yes"])

# Convert Yes/No to binary
ai = 1 if interest_ai == "Yes" else 0
cloud = 1 if interest_cloud == "Yes" else 0

if st.button("🎯 Suggest Career"):
    prediction = model.predict([[math_score, coding_skill, ai, cloud]])
    st.success(f"✅ Suggested Career: **{prediction[0]}**")
>>>>>>> 160a65b (new update)
