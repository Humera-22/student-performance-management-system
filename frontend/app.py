import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="Student Performance System", layout="centered")
st.title("🎓 Student Performance Management System")

# =====================================================
# STUDENT SECTION
# =====================================================
st.header("👤 Student Management")

with st.expander("➕ Add Student"):
    name = st.text_input("Student Name", key="student_name")
    email = st.text_input("Student Email", key="student_email")

    if st.button("Add Student"):
        response = requests.post(
            f"{API_URL}/students",
            json={"name": name, "email": email}
        )
        if response.status_code == 201:
            st.success("Student added successfully")
        else:
            st.error(response.json().get("error", "Failed"))

with st.expander("📋 View Students"):
    if st.button("Fetch Students"):
        res = requests.get(f"{API_URL}/students")
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch students")

# =====================================================
# COURSE SECTION
# =====================================================
st.header("📘 Course Management")

with st.expander("➕ Add Course"):
    title = st.text_input("Course Title", key="course_title")

    if st.button("Add Course"):
        res = requests.post(
            f"{API_URL}/courses",
            json={"title": title}
        )
        if res.status_code == 201:
            st.success("Course added successfully")
        else:
            st.error("Failed to add course")

with st.expander("📋 View Courses"):
    if st.button("Fetch Courses"):
        res = requests.get(f"{API_URL}/courses")
        if res.status_code == 200:
            st.table(res.json())
        else:
            st.error("Failed to fetch courses")

# =====================================================
# PERFORMANCE SECTION
# =====================================================
st.header("📊 Performance Management")

with st.expander("➕ Add Performance"):
    student_id = st.number_input("Student ID", min_value=1, step=1, key="perf_student")
    course_id = st.number_input("Course ID", min_value=1, step=1, key="perf_course")
    marks = st.number_input("Marks", min_value=0, max_value=100, step=1, key="perf_marks")

    if st.button("Add Performance"):
        res = requests.post(
            f"{API_URL}/performance",
            json={
                "student_id": student_id,
                "course_id": course_id,
                "marks": marks
            }
        )
        if res.status_code == 201:
            st.success("Performance added successfully")
        else:
            st.error("Failed to add performance")

with st.expander("📋 View Performance Records"):
    if st.button("Fetch Performance"):
        res = requests.get(f"{API_URL}/performance")
        if res.status_code == 200:
            data = res.json()

            # Hide internal performance ID for UI clarity
            clean_data = [
                {
                    "Student ID": p["student_id"],
                    "Course ID": p["course_id"],
                    "Marks": p["marks"]
                }
                for p in data
            ]

            if clean_data:
                st.table(clean_data)
            else:
                st.info("No performance records found")
        else:
            st.error("Failed to fetch performance")
