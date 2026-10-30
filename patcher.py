import os

APP_PATH = "app.py"

SECURE_SQL_PATCH = '''@app.get("/api/search")
def search_user(username: str = Query(..., description="Username to search")):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # SECURED: Parameterized query prevents SQL injection
    query = "SELECT id, username, role, credit_card FROM users WHERE username = ?"
    try:
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        conn.close()
        return {"status": "success", "results": results}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))'''

VULN_SQL_BLOCK = '''@app.get("/api/search")
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
        raise HTTPException(status_code=500, detail=str(e))'''

def apply_patch():
    if not os.path.exists(APP_PATH):
        return False, "app.py not found"
    
    with open(APP_PATH, "r") as f:
        content = f.read()
        
    import os

APP_PATH = "app.py"

VULN_SEARCH_BLOCK = '''@app.get("/api/search")
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
        raise HTTPException(status_code=500, detail=str(e))'''

SECURE_SEARCH_BLOCK = '''@app.get("/api/search")
def search_user(username: str = Query(..., description="Username to search")):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # SECURED: Parameterized query prevents SQL injection
    query = "SELECT id, username, role, credit_card FROM users WHERE username = ?"
    try:
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        conn.close()
        return {"status": "success", "results": results}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))'''

def apply_patch():
    if not os.path.exists(APP_PATH):
        return False, "app.py not found"
    with open(APP_PATH, "r") as f:
        content = f.read()
    
    if "SECURED: Parameterized query" in content:
        return True, "Patch already applied!"
    
    if VULN_SEARCH_BLOCK in content:
        new_content = content.replace(VULN_SEARCH_BLOCK, SECURE_SEARCH_BLOCK)
        with open(APP_PATH, "w") as f:
            f.write(new_content)
        return True, "Successfully applied SQL Injection secure parameterized fix!"
    else:
        return False, "Could not match vulnerable block signature."

def revert_patch():
    if not os.path.exists(APP_PATH):
        return False, "app.py not found"
    with open(APP_PATH, "r") as f:
        content = f.read()
    
    if "VULNERABLE: Direct string formatting" in content:
        return True, "Already in vulnerable state!"
        
    if SECURE_SEARCH_BLOCK in content:
        new_content = content.replace(SECURE_SEARCH_BLOCK, VULN_SEARCH_BLOCK)
        with open(APP_PATH, "w") as f:
            f.write(new_content)
        return True, "Reverted patch back to vulnerable state for demo!"
    else:
        return False, "Could not match secure block signature to revert."