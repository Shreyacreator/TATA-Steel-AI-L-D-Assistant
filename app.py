import os
import pandas as pd
import streamlit as st
import requests

from rag_utils import build_vector_store, retrieve_context

# Streamlit page layout config
st.set_page_config(
    page_title="AI L&D Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered L&D Assistant ")
st.write("Personalized learning and real-time training support for Tata Steel industrial workforce.")

@st.cache_data
def load_employees():
    return pd.read_csv("employee_dataset.csv")

@st.cache_resource
def load_vector_store():
    return build_vector_store("knowledge_base")

# Load employee dataset and local vector database
employees = load_employees()
index, chunks = load_vector_store()

# --- SIDEBAR: Employee Profile ---
with st.sidebar:
    st.header("Employee Profile")
    emp_id = st.selectbox("Select Employee", employees["Emp_ID"])
    profile = employees[employees["Emp_ID"] == emp_id].iloc[0]

    current_role = profile['Role']
    st.write(f"**Role:** {current_role}")
    st.write(f"**Experience:** {profile['Experience_Years']} years")
    st.write(f"**Skill Score:** {profile['Skill_Score']}")
    st.write(f"**Language:** {profile['Preferred_Language']}")

# --- MAIN CONTENT: Personalized Recommendation ---
st.subheader("📚 Personalized Recommendation")
st.success(f"Recommended Training: {profile['Recommended_Training']}")

st.write("---")

# --- SECTION 1: FIXED QUESTIONS (FROM SQL DB) ---
st.subheader("❓ Standard Profile Questions ")

fixed_questions = []
try:
    # Local FastAPI server se questions load karna
    response = requests.get(f"http://127.0.0.1:8000/get-questions/{current_role}")
    if response.status_code == 200:
        fixed_questions = response.json().get("questions", [])
except Exception:
    st.error("⚠️ Backend API server running nahi hai! Please VS Code terminal mein jaakar 'uvicorn api:app --reload --port 8000' run karein.")

selected_fixed_q = None
if fixed_questions:
    options = ["-- Select a standard question --"] + fixed_questions
    selected_fixed_q = st.selectbox("Choose a frequently asked question for your profile:", options)

# --- SECTION 2: CUSTOM INPUT BOX ---
st.subheader("🌐 Ask a Custom Training Question")
custom_question = st.text_input("Type your own specific query here (e.g., safety, guidelines):")

# --- PROCESSING LOGIC (NO GEMINI USED) ---
final_question = None
is_db_query = False

# Preference check: Agar custom input khali nahi hai toh use pehle process karenge
if custom_question.strip():
    final_question = custom_question.strip()
    is_db_query = False
elif selected_fixed_q and selected_fixed_q != "-- Select a standard question --":
    final_question = selected_fixed_q
    is_db_query = True

# Jab user ka sawal ready ho
if final_question:
    st.write("---")
    with st.spinner("Processing your request..."):
        
        # CASE A: Agar dropdown wala standard question select kiya hai
        if is_db_query:
            try:
                api_payload = {"role": current_role, "question": final_question}
                res = requests.post("http://127.0.0.1:8000/ask-agent", json=api_payload)
                
                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f"### 🗄️ System Response ({data['source']})")
                    st.info(data["answer"])
            except Exception as e:
                st.error(f"Database fetch karne mein dikkat aayi: {e}")
                
        # CASE B: Agar user ne apna khudka custom question type kiya hai (RAG Search)
        else:
            # Aapke rag_utils.py ka use karke local PDF chunks se accurate material dhoondhna
            context = retrieve_context(final_question, index, chunks)
            
            st.markdown("### 🔍 Local Knowledge Base Search Results")
            if context.strip():
                st.success("Found matching standard operating procedures (SOPs) inside your PDFs:")
                st.markdown(f"> {context}")
                
                # Pro Tips structure user experience improve karne ke liye
                with st.expander("💡 Smart Recommendation Based on Your Profile:"):
                    st.write(f"As a **{current_role}** with **{profile['Experience_Years']} years** of experience, you should thoroughly review this SOP context before entering the operational bay. Recommended Module: **{profile['Recommended_Training']}**.")
            else:
                st.warning("No relevant matching context found in the local PDF 'knowledge_base' folder for this query. Please try searching with industrial keywords like 'safety', 'PPE', 'crane', etc.")