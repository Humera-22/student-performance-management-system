"""
from app.models import Course
from app import db
from .base import BaseService

class CourseService(BaseService):

    @classmethod
    def create(cls, data):
        course = Course(**data)
        db.session.add(course)
        db.session.commit()
        return course

    @classmethod
    def update(cls, course, data):
        course.title = data.get("title", course.title)
        db.session.commit()
        return course
"""
# app/services/course.py
from app.models import Course
from app import db
from .base import BaseService
from app.exceptions import AppException

class CourseService(BaseService):

    @classmethod
    def create(cls, data):
        try:
            course = Course(**data)
            db.session.add(course)
            db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to create course: {str(e)}")

    @classmethod
    def update(cls, course, data):
        try:
            course.title = data.get("title", course.title)
            db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to update course: {str(e)}")
