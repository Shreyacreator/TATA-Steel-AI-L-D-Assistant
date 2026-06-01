from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Tata Steel Digital Guide API")

class QueryRequest(BaseModel):
    role: str
    question: str

def query_db_for_faq(role: str, question: str):
    conn = sqlite3.connect("tatasteel_ld.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Exact match check karega database mein
    cursor.execute(
        "SELECT answer FROM fixed_faqs WHERE LOWER(role) = LOWER(?) AND LOWER(question) = LOWER(?)", 
        (role, question)
    )
    row = cursor.fetchone()
    conn.close()
    return row["answer"] if row else None

def get_all_questions_by_role(role: str):
    conn = sqlite3.connect("tatasteel_ld.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT question FROM fixed_faqs WHERE LOWER(role) = LOWER(?)", (role,))
    rows = cursor.fetchall()
    conn.close()
    return [row["question"] for row in rows]

# Endpoint 1: Role select karne par uske fixed questions dropdown mein dikhane ke liye
@app.get("/get-questions/{role}")
def get_questions(role: str):
    questions = get_all_questions_by_role(role)
    return {"questions": questions}

# Endpoint 2: Answer fetch karne ke liye (Database ya Dynamic AI)
@app.post("/ask-agent")
def ask_agent(request: QueryRequest):
    # Sabse pehle DB mein fixed questions check karo
    db_answer = query_db_for_faq(request.role, request.question)
    
    if db_answer:
        return {
            "source": "Local Database (Fixed FAQ)",
            "answer": db_answer
        }
    
    # Agar DB mein nahi mila, toh aap dynamic processing (RAG) return kar sakte hain
    return {
        "source": "Dynamic Query Needed",
        "answer": None
    }