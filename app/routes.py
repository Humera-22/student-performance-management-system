# app/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Student, Course, Performance, User
from app.auth import jwt_required, role_required, generate_token
from app.utils import Utils
from app.dataclasses import StudentRequest, CourseRequest, PerformanceRequest
from dataclasses import asdict
import requests

api = Blueprint("api", __name__)

# -------------------------
# AUTH
# -------------------------
@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"access_token": token}), 200

# -------------------------
# STUDENTS
# -------------------------
# -------------------------
# GET Students (viewable by admin & user)
# -------------------------
@api.route("/students", methods=["GET"])
@jwt_required
@role_required(["admin", "user"])
def get_students():
    cached = Utils.get_cache("students")
    if cached:
        return jsonify(cached)
    students = Student.query.all()
    result = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    Utils.set_cache("students", result)
    return jsonify(result)

# -------------------------
# Create Student (admin only)
# -------------------------
@api.route("/students", methods=["POST"])
@jwt_required
@role_required(["admin"])
def create_student():
    try:
        data = StudentRequest(**request.get_json())
        student = Student(**asdict(data))
        db.session.add(student)
        db.session.commit()
        Utils.redis_client.delete("students")  # Invalidate cache
        return jsonify({"message": "Student created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------
# Update Student (admin only)
# -------------------------
@api.route("/students/<int:id>", methods=["PUT"])
@jwt_required
@role_required(["admin"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    try:
        data = StudentRequest(**request.get_json())
        student.name = data.name
        student.email = data.email
        db.session.commit()
        Utils.redis_client.delete("students")  # Invalidate cache
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------
# Delete Student (admin only)
# -------------------------
@api.route("/students/<int:id>", methods=["DELETE"])
@jwt_required
@role_required(["admin"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        Utils.redis_client.delete("students")  # Invalidate cache
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------
# COURSES
# -------------------------
@api.route("/courses", methods=["GET"])
@jwt_required
@role_required(["admin", "user"])
def get_courses():
    cached = Utils.get_cache("courses")
    if cached:
        return jsonify(cached)
    courses = Course.query.all()
    result = [{"id": c.id, "title": c.title} for c in courses]
    Utils.set_cache("courses", result)
    return jsonify(result)

@api.route("/courses", methods=["POST"])
@jwt_required
@role_required(["admin"])
def create_course():
    try:
        data = CourseRequest(**request.get_json())
        course = Course(**asdict(data))
        db.session.add(course)
        db.session.commit()
        Utils.redis_client.delete("courses")
        return jsonify({"message": "Course created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------
# PERFORMANCE
# -------------------------
@api.route("/performance", methods=["GET"])
@jwt_required
@role_required(["admin", "user"])
def get_performance():
    cached = Utils.get_cache("performance")
    if cached:
        return jsonify(cached)
    performances = Performance.query.all()
    result = [{"student_id": p.student_id, "course_id": p.course_id, "marks": p.marks} for p in performances]
    Utils.set_cache("performance", result)
    return jsonify(result)

@api.route("/performance", methods=["POST"])
@jwt_required
@role_required(["admin"])
def add_performance():
    try:
        data = PerformanceRequest(**request.get_json())
        performance = Performance(**asdict(data))
        db.session.add(performance)
        db.session.commit()
        Utils.redis_client.delete("performance")
        return jsonify({"message": "Performance added"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------
# USERS
# -------------------------
@api.route("/users", methods=["POST"])
@jwt_required
@role_required(["admin"])
def create_user():
    data = request.get_json()
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=data["username"], is_admin=False)
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Normal user created"}), 201

# -------------------------
# EXTERNAL API
# -------------------------
@api.route("/get-info", methods=["GET"])
@jwt_required
@role_required(["admin", "user"])
def get_info():
    try:
        res = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
