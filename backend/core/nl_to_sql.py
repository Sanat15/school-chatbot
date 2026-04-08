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
    # If LLM returns "SQLQuery: SELECT ..." extract just the SQL
    if "SQLQuery:" in raw:
        raw = raw.split("SQLQuery:")[-1]
    # Remove markdown code blocks
    raw = re.sub(r"```sql|```", "", raw)
    # Remove any "Question: ..." line at the start
    lines = [l for l in raw.strip().splitlines() if not l.strip().lower().startswith("question:")]
    return "\n".join(lines).strip()

def run_nl_query(question: str):
    chain, db = get_db_chain()
    raw = chain.invoke({"question": question})
    sql_query = clean_sql(raw)
    result = db.run(sql_query)
    return {"query": sql_query, "result": result}