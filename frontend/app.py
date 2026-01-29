# app.py
import streamlit as st
import requests
import jwt

# -------------------------
# CONFIG
# -------------------------
API_URL = "http://127.0.0.1:5000"
HEADERS = {"Content-Type": "application/json"}

st.set_page_config(
    page_title="Student Performance System",
    layout="centered"
)

st.title("🎓 Student Performance Management System")

# -------------------------
# SESSION STATE
# -------------------------
if "token" not in st.session_state:
    st.session_state.token = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# -------------------------
# LOGIN SECTION
# -------------------------
if not st.session_state.token:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/api/login",
            json={"username": username, "password": password},
            headers=HEADERS
        )
        if res.status_code == 200:
            token = res.json()["access_token"]
            payload = jwt.decode(token, options={"verify_signature": False})
            st.session_state.token = token
            st.session_state.is_admin = payload.get("is_admin", False)
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# -------------------------
# AUTH HEADER
# -------------------------
auth_headers = {
    "Authorization": f"Bearer {st.session_state.token}",
    "Content-Type": "application/json"
}

# -------------------------
# ROLE INFO
# -------------------------
if st.session_state.is_admin:
    st.success("👑 Logged in as Admin")
else:
    st.info("👤 Logged in as Normal User")

# -------------------------
# STUDENT SECTION
# -------------------------
st.header("👤 Student Management")

if st.session_state.is_admin:
    with st.expander("➕ Add Student"):
        name = st.text_input("Student Name", key="add_name")
        email = st.text_input("Student Email", key="add_email")
        if st.button("Add Student"):
            res = requests.post(f"{API_URL}/api/students", json={"name": name, "email": email}, headers=auth_headers)
            if res.status_code == 201:
                st.success("Student added successfully")
            else:
                st.error(res.json().get("error", "Failed"))

    with st.expander("✏️ Update Student"):
        student_id = st.number_input("Student ID", min_value=1, step=1, key="update_id")
        name = st.text_input("New Name", key="update_name")
        email = st.text_input("New Email", key="update_email")
        if st.button("Update Student"):
            res = requests.put(f"{API_URL}/api/students/{student_id}", json={"name": name, "email": email}, headers=auth_headers)
            if res.status_code == 200:
                st.success("Student updated successfully")
            else:
                st.error(res.json().get("error", "Failed"))

    with st.expander("🗑 Delete Student"):
        student_id = st.number_input("Student ID to Delete", min_value=1, step=1, key="delete_id")
        if st.button("Delete Student"):
            res = requests.delete(f"{API_URL}/api/students/{student_id}", headers=auth_headers)
            if res.status_code == 200:
                st.success("Student deleted successfully")
            else:
                st.error(res.json().get("error", "Failed"))

with st.expander("📋 View Students"):
    if st.button("Fetch Students"):
        res = requests.get(f"{API_URL}/api/students", headers=auth_headers)
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch students")

# -------------------------
# COURSE SECTION
# -------------------------
st.header("📘 Course Management")

if st.session_state.is_admin:
    with st.expander("➕ Add Course"):
        title = st.text_input("Course Title", key="course_add")
        if st.button("Add Course"):
            res = requests.post(f"{API_URL}/api/courses", json={"title": title}, headers=auth_headers)
            if res.status_code == 201:
                st.success("Course added successfully")
            else:
                st.error(res.json().get("error", "Failed"))

with st.expander("📋 View Courses"):
    if st.button("Fetch Courses"):
        res = requests.get(f"{API_URL}/api/courses", headers=auth_headers)
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch courses")

# -------------------------
# PERFORMANCE SECTION
# -------------------------
st.header("📊 Performance Management")

if st.session_state.is_admin:
    with st.expander("➕ Add Performance"):
        student_id = st.number_input("Student ID", min_value=1, step=1, key="perf_student")
        course_id = st.number_input("Course ID", min_value=1, step=1, key="perf_course")
        marks = st.number_input("Marks", min_value=0, max_value=100, step=1, key="perf_marks")
        if st.button("Add Performance"):
            res = requests.post(f"{API_URL}/api/performance",
                                json={"student_id": student_id, "course_id": course_id, "marks": marks},
                                headers=auth_headers)
            if res.status_code == 201:
                st.success("Performance added successfully")
            else:
                st.error(res.json().get("error", "Failed"))

with st.expander("📋 View Performance Records"):
    if st.button("Fetch Performance"):
        res = requests.get(f"{API_URL}/api/performance", headers=auth_headers)
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch performance")

# -------------------------
# EXTERNAL API
# -------------------------
st.header("🌐 External API Example")
if st.button("Fetch /get-info"):
    res = requests.get(f"{API_URL}/api/get-info", headers=auth_headers)
    if res.status_code == 200:
        st.json(res.json())
    else:
        st.error("Failed to fetch external info")

# -------------------------
# LOGOUT
# -------------------------
if st.button("🚪 Logout"):
    st.session_state.token = None
    st.session_state.is_admin = False
    st.success("Logged out successfully")
    st.rerun()
