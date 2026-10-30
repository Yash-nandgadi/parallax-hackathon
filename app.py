import os
import sqlite3
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="PatchProof Vulnerable Fixture", version="1.0.0")

DB_FILE = "test_app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, credit_card TEXT)")
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (username, role, credit_card) VALUES ('alice', 'user', '4111-2222-3333-4444')")
    cursor.execute("INSERT INTO users (username, role, credit_card) VALUES ('admin', 'admin', '5555-4433-2211-0000')")
    conn.commit()
    conn.close()

init_db()

# --- VULNERABILITY 1: SQL Injection (CWE-89) ---
@app.get("/api/search")
def search_user(username: str = Query(..., description="Username to search")):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # VULNERABLE: Direct string formatting into SQL query
    query = f"SELECT id, username, role, credit_card FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return {"status": "success", "results": results}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))  

# --- VULNERABILITY 2: Path Traversal (CWE-22) ---
@app.get("/api/download")
def download_file(filepath: str = Query(..., description="File to download")):
    # VULNERABLE: Direct path concatenation allows directory traversal (e.g., ../../etc/passwd)
    target_path = os.path.join("storage", filepath)
    if os.path.exists(target_path) and os.path.isfile(target_path):
        with open(target_path, "r") as f:
            content = f.read()
        return {"status": "success", "file_content": content}
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)