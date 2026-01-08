from app import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationship: One student → many performances
    performances = db.relationship(
        "Performance",
        backref="student",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Student {self.name}>"


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # Relationship: One course → many performances
    performances = db.relationship(
        "Performance",
        backref="course",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Course {self.title}>"


class Performance(db.Model):
    __tablename__ = "performances"

    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)

    # Foreign Keys
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Performance StudentID={self.student_id} CourseID={self.course_id}>"

