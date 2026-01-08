from flask import Blueprint, request, jsonify
from app import db
from app.models import Student, Course, Performance

api = Blueprint("api", __name__)

# -------------------------
# STUDENT CRUD
# -------------------------

@api.route("/students", methods=["POST"])
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

        return jsonify({"message": "Student created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@api.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "email": s.email}
        for s in students
    ])


@api.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON body is required"}), 400

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
        return jsonify({"message": "Student updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@api.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({"error": "Student not found"}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# -------------------------
# COURSE CRUD
# -------------------------

@api.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json()
    course = Course(title=data["title"])
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course created"}), 201


@api.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {"id": c.id, "title": c.title}
        for c in courses
    ])


# -------------------------
# PERFORMANCE CRUD
# -------------------------

@api.route("/performance", methods=["POST"])
def add_performance():
    data = request.get_json()
    performance = Performance(
        marks=data["marks"],
        student_id=data["student_id"],
        course_id=data["course_id"]
    )
    db.session.add(performance)
    db.session.commit()
    return jsonify({"message": "Performance added"}), 201


@api.route("/performance", methods=["GET"])
def get_performance():
    records = Performance.query.all()
    return jsonify([
        {
            "id": p.id,
            "marks": p.marks,
            "student_id": p.student_id,
            "course_id": p.course_id
        }
        for p in records
    ])

