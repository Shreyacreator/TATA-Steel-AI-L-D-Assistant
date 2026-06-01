# 🏗️ Tata Steel AI-Powered L&D Assistant & Digital Guide

An intelligent, secure, and 100% local AI Agent designed to provide personalized learning, safety guidelines, and real-time training support for the industrial workforce at Tata Steel.

## 🚀 Key Features
* **Role-Based Personalization:** Automatically detects employee profile (from a dataset of 25 departments) and serves custom recommendations.
* **Hybrid Architecture:** 
  * **Fast & Cost-Effective:** Fetches standard profile-specific FAQs directly from a local **SQLite Database** using **FastAPI**.
  * **Smart Custom Search:** Uses an offline **FAISS Vector Store** and `SentenceTransformer` to query industrial PDFs/SOPs via RAG (Retrieval-Augmented Generation).
* **Privacy Focused:** 100% offline compliance—no external AI website APIs used, ensuring corporate data safety and zero billing costs.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend API:** FastAPI & Uvicorn
* **Database:** SQLite (SQL)
* **Vector Search:** FAISS & PyPDF2

## 📦 How to Run Locally
1. Clone the repository and install requirements:
```bash
   pip install -r requirements.txt
