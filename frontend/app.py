import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/api"

st.set_page_config(
    page_title="Student Performance System",
    layout="centered"
)

st.title("🎓 Student Performance Management System")

# =====================================================
# AUTH SECTION
# =====================================================

st.header("🔐 Authentication")

if "token" not in st.session_state:
    st.session_state.token = None

if st.button("Get JWT Token"):
    res = requests.get(f"{API_URL}/token")
    if res.status_code == 200:
        st.session_state.token = res.json()["token"]
        st.success("Token generated successfully")
    else:
        st.error("Failed to generate token")

if not st.session_state.token:
    st.warning("Please generate token to access APIs")
    st.stop()

headers = {
    "Authorization": st.session_state.token
}

# =====================================================
# STUDENT SECTION
# =====================================================

st.header("👤 Student Management")

with st.expander("➕ Add Student"):
    name = st.text_input("Student Name")
    email = st.text_input("Student Email")

    if st.button("Add Student"):
        res = requests.post(
            f"{API_URL}/students",
            json={"name": name, "email": email},
            headers=headers
        )
        if res.status_code == 201:
            st.success("Student added successfully")
        else:
            st.error(res.json().get("error", "Failed"))

with st.expander("📋 View Students"):
    if st.button("Fetch Students"):
        res = requests.get(f"{API_URL}/students", headers=headers)
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch students")

# =====================================================
# COURSE SECTION
# =====================================================

st.header("📘 Course Management")

with st.expander("➕ Add Course"):
    title = st.text_input("Course Title")

    if st.button("Add Course"):
        res = requests.post(
            f"{API_URL}/courses",
            json={"title": title},
            headers=headers
        )
        if res.status_code == 201:
            st.success("Course added successfully")
        else:
            st.error("Failed to add course")

with st.expander("📋 View Courses"):
    if st.button("Fetch Courses"):
        res = requests.get(f"{API_URL}/courses", headers=headers)
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch courses")

# =====================================================
# PERFORMANCE SECTION
# =====================================================

st.header("📊 Performance Management")

with st.expander("➕ Add Performance"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    course_id = st.number_input("Course ID", min_value=1, step=1)
    marks = st.number_input("Marks", min_value=0, max_value=100, step=1)

    if st.button("Add Performance"):
        res = requests.post(
            f"{API_URL}/performance",
            json={
                "student_id": student_id,
                "course_id": course_id,
                "marks": marks
            },
            headers=headers
        )
        if res.status_code == 201:
            st.success("Performance added successfully")
        else:
            st.error("Failed to add performance")


with st.expander("📋 View Performance Records"):
    if st.button("Fetch Performance"):
        res = requests.get(f"{API_URL}/performance", headers=headers)
        if res.status_code == 200:
            data = res.json()
            clean_data = [
                {
                    "Student ID": p["student_id"],
                    "Course ID": p["course_id"],
                    "Marks": p["marks"]
                }
                for p in data
            ]
            st.table(clean_data)
        else:
            st.error("Failed to fetch performance")
