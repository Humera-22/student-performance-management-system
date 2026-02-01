# app/routes.py
from flask import Blueprint, request, jsonify, g
from dataclasses import asdict

from app import db
from app.models import User, Student, Course, Performance
from app.dataclasses import (
    StudentRequest, CourseRequest, PerformanceRequest,
    StudentResponse, CourseResponse, PerformanceResponse, UserRequest, UserResponse
)
from app.utils import Utils
from app.http_client import HttpClient
from app.auth.decorators import jwt_required, roles_required
from app.auth.jwt import generate_token
from app.services.student import StudentService
from app.services.course import CourseService
from app.services.performance import PerformanceService

api = Blueprint("api", __name__)

# -------------------------
# AUTHENTICATION
# -------------------------
@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"access_token": token}), 200


# -------------------------
# STUDENTS
# -------------------------
@api.route("/students", methods=["GET"])
@jwt_required
@roles_required(["admin", "teacher", "principal", "student"])
def get_students():
    cached = Utils.get_cache("students")
    if cached:
        return jsonify(cached)

    students = Student.query.all()
    result = [asdict(StudentResponse(id=s.id, name=s.name, email=s.email)) for s in students]
    Utils.set_cache("students", result)
    return jsonify(result)


@api.route("/students", methods=["POST"])
@jwt_required
@roles_required(["admin", "principal"])
def create_student():
    data = StudentRequest(**request.get_json())
    StudentService.create(asdict(data))
    Utils.delete_cache("students")
    return jsonify({"message": "Student created"}), 201


@api.route("/students/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(["admin", "principal", "student"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Only allow student to update self
    if "student" in g.roles and g.user_id != id:
        return jsonify({"error": "Forbidden"}), 403

    data = StudentRequest(**request.get_json())
    StudentService.update(student, asdict(data))
    Utils.delete_cache("students")
    return jsonify({"message": "Student updated"}), 200


@api.route("/students/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(["admin", "principal"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    StudentService.delete(student)
    Utils.delete_cache("students")
    return jsonify({"message": "Student deleted"}), 200


# -------------------------
# COURSES
# -------------------------
@api.route("/courses", methods=["GET"])
@jwt_required
@roles_required(["admin", "teacher", "principal", "student"])
def get_courses():
    cached = Utils.get_cache("courses")
    if cached:
        return jsonify(cached)

    courses = Course.query.all()
    result = [asdict(CourseResponse(id=c.id, title=c.title)) for c in courses]
    Utils.set_cache("courses", result)
    return jsonify(result)


@api.route("/courses", methods=["POST"])
@jwt_required
@roles_required(["admin", "principal"])
def create_course():
    data = CourseRequest(**request.get_json())
    CourseService.create(asdict(data))
    Utils.delete_cache("courses")
    return jsonify({"message": "Course created"}), 201


# -------------------------
# PERFORMANCE
# -------------------------
@api.route("/performance", methods=["GET"])
@jwt_required
@roles_required(["admin", "teacher", "principal", "student"])
def get_performance():
    cached = Utils.get_cache("performance")
    if cached:
        return jsonify(cached)

    performances = Performance.query.all()
    result = [
        asdict(PerformanceResponse(student_id=p.student_id, course_id=p.course_id, marks=p.marks))
        for p in performances
    ]
    Utils.set_cache("performance", result)
    return jsonify(result)


@api.route("/performance", methods=["POST"])
@jwt_required
@roles_required(["admin", "teacher"])
def add_performance():
    data = PerformanceRequest(**request.get_json())
    PerformanceService.create(asdict(data))
    Utils.delete_cache("performance")
    return jsonify({"message": "Performance added"}), 201


# -------------------------
# USERS
# -------------------------
@api.route("/users", methods=["POST"])
@jwt_required
@roles_required(["admin"])
def create_user():
    data = UserRequest(**request.get_json())
    if User.query.filter_by(username=data.username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=data.username, roles=data.roles)
    user.set_password(data.password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


# -------------------------
# EXTERNAL API
# -------------------------
@api.route("/get-info", methods=["GET"])
@jwt_required
@roles_required(["admin", "teacher", "principal", "student"])
def get_info():
    data = HttpClient.get("https://jsonplaceholder.typicode.com/posts/1")
    return jsonify(data)
