"""
from app.models import Student
from app import db
from .base import BaseService

class StudentService(BaseService):

    @classmethod
    def create(cls, data):
        student = Student(**data)
        db.session.add(student)
        db.session.commit()
        return student

    @classmethod
    def update(cls, student, data):
        student.name = data.get("name", student.name)
        student.email = data.get("email", student.email)
        db.session.commit()
        return student
"""
# app/services/student.py
from app.models import Student
from app import db
from .base import BaseService
from app.exceptions import AppException

class StudentService(BaseService):

    @classmethod
    def create(cls, data):
        try:
            student = Student(**data)
            db.session.add(student)
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to create student: {str(e)}")

    @classmethod
    def update(cls, student, data):
        try:
            student.name = data.get("name", student.name)
            student.email = data.get("email", student.email)
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to update student: {str(e)}")

