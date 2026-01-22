from flask import Blueprint, request, jsonify
from app import db
from app.models import Student, Course, Performance
from app.auth import jwt_required, generate_token
from app.cache import get_cache, set_cache, redis_client

api = Blueprint("api", __name__)

# -------------------------
# AUTH
# -------------------------

@api.route("/token", methods=["GET"])
def get_token():
    token = generate_token()
    return jsonify({"token": token})


# -------------------------
# STUDENT CRUD
# -------------------------

@api.route("/students", methods=["POST"])
@jwt_required
def create_student():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON body is required"}), 400

        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            return jsonify({"error": "Email already exists"}), 409

        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()

        redis_client.delete("students")
        return jsonify({"message": "Student created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api.route("/students", methods=["GET"])
@jwt_required
def get_students():
    cached_data = get_cache("students")
    if cached_data:
        return jsonify(cached_data)

    students = Student.query.all()
    result = [{"id": s.id, "name": s.name, "email": s.email} for s in students]

    set_cache("students", result)
    return jsonify(result)


@api.route("/students/<int:id>", methods=["PUT"])
@jwt_required
def update_student(id):
    try:
        data = request.get_json()

        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        name = data.get("name")
        email = data.get("email")

        if email:
            existing_student = Student.query.filter_by(email=email).first()
            if existing_student and existing_student.id != id:
                return jsonify({"error": "Email already exists"}), 409

        student.name = name or student.name
        student.email = email or student.email

        db.session.commit()
        redis_client.delete("students")
        return jsonify({"message": "Student updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api.route("/students/<int:id>", methods=["DELETE"])
@jwt_required
def delete_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        db.session.delete(student)
        db.session.commit()
        redis_client.delete("students")

        return jsonify({"message": "Student deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -------------------------
# COURSE CRUD
# -------------------------

@api.route("/courses", methods=["POST"])
@jwt_required
def create_course():
    data = request.get_json()
    course = Course(title=data["title"])
    db.session.add(course)
    db.session.commit()

    redis_client.delete("courses")
    return jsonify({"message": "Course created"}), 201


@api.route("/courses", methods=["GET"])
@jwt_required
def get_courses():
    cached_data = get_cache("courses")
    if cached_data:
        return jsonify(cached_data)

    courses = Course.query.all()
    result = [{"id": c.id, "title": c.title} for c in courses]

    set_cache("courses", result)
    return jsonify(result)

# -------------------------
# PERFORMANCE CRUD
# -------------------------

@api.route("/performance", methods=["POST"])
@jwt_required
def add_performance():
    data = request.get_json()
    performance = Performance(
        marks=data["marks"],
        student_id=data["student_id"],
        course_id=data["course_id"]
    )
    db.session.add(performance)
    db.session.commit()

    redis_client.delete("performance")
    return jsonify({"message": "Performance added"}), 201


@api.route("/performance", methods=["GET"])
@jwt_required
def get_performance():
    cached_data = get_cache("performance")
    if cached_data:
        return jsonify(cached_data)

    records = Performance.query.all()
    result = [
        {
            "id": p.id,
            "marks": p.marks,
            "student_id": p.student_id,
            "course_id": p.course_id
        }
        for p in records
    ]

    set_cache("performance", result)
    return jsonify(result)


