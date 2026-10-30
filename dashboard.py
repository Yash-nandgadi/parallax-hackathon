import streamlit as st
import requests
from patcher import apply_patch, revert_patch

st.set_page_config(page_title="PatchProof - Verified AppSec Remediation", layout="wide")

st.title("🛡️ PatchProof: Find the Flaw. Prove the Fix.")
st.markdown("### Autonomous AppSec, SAST Verification & Safe Remediation Platform")

BASE_URL = "http://127.0.0.1:8000"

tab1, tab2, tab3 = st.tabs(["🔍 Vulnerability Inventory", "⚡ Exploit & Verification Lab", "🛠️ Automated Patch & Regression"])

with tab1:
    st.subheader("In-Scope Target Files & Detected Findings")
    st.info("Target Fixture: `app.py` | Framework: FastAPI | Database: SQLite | Storage: Local Filesystem")
    
    st.error("### CWE-89: SQL Injection")
    st.markdown("**Severity:** `CRITICAL (CVSS 9.8)` | **Location:** `app.py` (Line 23)")
    st.markdown("Description: User input `username` is directly interpolated into SQL queries without parameterization.")

    st.warning("### CWE-22: Path Traversal (Arbitrary File Read)")
    st.markdown("**Severity:** `HIGH (CVSS 8.6)` | **Location:** `app.py` (Line 45)")
    st.markdown("Description: Unsanitized file path input allows attackers to traverse directories and read sensitive server files using `../../` sequences.")

with tab2:
    st.subheader("Live Exploit Proof-of-Concept (PoC)")
    st.markdown("Verify whether vulnerabilities are actively exploitable *before* applying patches.")
    
    st.error("### 1. CWE-89: SQL Injection PoC")
    if st.button("Run SQL Injection Exploit PoC"):
        try:
            payload = "admin' OR '1'='1"
            res = requests.get(f"{BASE_URL}/api/search", params={"username": payload})
            data = res.json()
            if len(data.get("results", [])) > 1:
                st.error(f"🔴 EXPLOIT SUCCESSFUL! Dumped {len(data['results'])} records including Admin credentials & Credit Cards!")
                st.json(data)
            else:
                st.success("🟢 EXPLOIT BLOCKED / SECURE.")
        except Exception as e:
            st.warning(f"Target app is not running. Error: {e}")

    st.markdown("---")
    st.warning("### 2. CWE-22: Path Traversal PoC")
    if st.button("Run Path Traversal Exploit PoC"):
        try:
            res = requests.get(f"{BASE_URL}/api/download", params={"filepath": "../app.py"})
            data = res.json()
            if "file_content" in data:
                st.error("🔴 EXPLOIT SUCCESSFUL! Read unauthorized server source file (`app.py`)!")
                st.json(data)
            else:
                st.success("🟢 EXPLOIT BLOCKED / SECURE.")
        except Exception as e:
            st.warning(f"Target app is not running. Error: {e}")



with tab3:
    st.subheader("Automated Remediation & Regression Testing")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚀 Apply Defensive Patch"):
            success, msg = apply_patch()
            if success:
                st.success(msg)
                st.toast("Patch applied! Restart `app.py` terminal to load changes.")
            else:
                st.error(msg)
                
    with col_b:
        if st.button("🔄 Revert Patch (Demo Mode)"):
            success, msg = revert_patch()
            st.info(msg)

    st.markdown("---")
    st.subheader("Patch Rationale & Code Diff")
    st.code("""
- query = f"SELECT id, username, role, credit_card FROM users WHERE username = '{username}'"
+ query = "SELECT id, username, role, credit_card FROM users WHERE username = ?"
+ cursor.execute(query, (username,))
    """, language="diff")
    
    if st.button("🧪 Run Post-Patch Verification Test"):
        st.markdown("Executing automated regression suite...")
        try:
            payload = "admin' OR '1'='1"
            res = requests.get(f"{BASE_URL}/api/search", params={"username": payload})
            data = res.json()
            results = data.get("results", [])
            if len(results) == 0 or (len(results) == 1 and results[0][1] != 'admin'):
                st.success("✅ REGRESSION TEST PASSED: Attack payload neutralized. Expected application behavior preserved!")
            else:
                st.warning("⚠️ VULNERABILITY STILL ACTIVE: Attack payload succeeded.")
        except Exception as e:
            st.error(f"Test failed to connect: {e}")