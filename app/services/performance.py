# app/services/performance.py
from app.models import Performance
from app import db
from .base import BaseService
from app.exceptions import AppException

class PerformanceService(BaseService):

    @classmethod
    def create(cls, data):
        try:
            performance = Performance(**data)
            db.session.add(performance)
            db.session.commit()
            return performance
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to add performance: {str(e)}")

    @classmethod
    def update(cls, performance, data):
        try:
            performance.marks = data.get("marks", performance.marks)
            performance.student_id = data.get("student_id", performance.student_id)
            performance.course_id = data.get("course_id", performance.course_id)
            db.session.commit()
            return performance
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to update performance: {str(e)}")
