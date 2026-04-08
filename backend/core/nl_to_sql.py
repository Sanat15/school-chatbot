from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from backend.core.llm import get_llm
from dotenv import load_dotenv
import re
import os

load_dotenv()

def get_db_chain():
    db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"))
    llm = get_llm()
    chain = create_sql_query_chain(llm, db)
    return chain, db

def clean_sql(raw: str) -> str:
    if "SQLQuery:" in raw:
        raw = raw.split("SQLQuery:")[-1]
    raw = re.sub(r"```sql|```", "", raw)
    lines = [l for l in raw.strip().splitlines() if not l.strip().lower().startswith("question:")]
    return "\n".join(lines).strip()

def generate_response(question: str, result: str, username: str) -> str:
    llm = get_llm()
    prompt = f"""You are a helpful school assistant chatbot.
A user named {username} asked: "{question}"
The database returned this result: {result}
Write a friendly, conversational response in 1-2 sentences using this data.
Do not mention SQL or databases. Just answer naturally."""
    response = llm.invoke(prompt)
    return response.content

def run_nl_query(question: str, username: str = "Student"):
    chain, db = get_db_chain()
    raw = chain.invoke({"question": question})
    sql_query = clean_sql(raw)
    result = db.run(sql_query)
    response = generate_response(question, result, username)
    return {"query": sql_query, "raw_result": result, "response": response}