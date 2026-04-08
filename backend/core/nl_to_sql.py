from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from backend.core.llm import get_llm
from dotenv import load_dotenv
import re
import os
from backend.core.language import detect_language

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
    lines = []
    for line in raw.strip().splitlines():
        stripped = line.strip().lower()
        # Stop at any non-SQL line
        if stripped.startswith("question:") or stripped.startswith("let's") or stripped.startswith("note:") or stripped.startswith("this query") or stripped.startswith("the above"):
            break
        lines.append(line)
    result = "\n".join(lines).strip()
    # Remove trailing semicolons issues - just take everything up to last semicolon
    if ";" in result:
        result = result[:result.rfind(";")+1]
    return result

def generate_response(question: str, result: str, username: str) -> str:
    llm = get_llm()
    lang = detect_language(question)
    prompt = f"""You are a helpful school assistant chatbot.
A user named {username} asked: "{question}"
The database returned this result: {result}
Write a friendly, conversational response in 1-2 sentences using this data.
IMPORTANT: Respond in {lang} language only.
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