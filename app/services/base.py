"""
from abc import ABC, abstractmethod
from app import db

class BaseService(ABC):
    Abstract base service providing common CRUD methods

    @classmethod
    @abstractmethod
    def create(cls, data):
        pass

    @classmethod
    @abstractmethod
    def update(cls, instance, data):
        pass

    @classmethod
    def delete(cls, instance):
        db.session.delete(instance)
        db.session.commit()
"""
# app/services/base.py
from abc import ABC, abstractmethod
from app import db
from app.exceptions import AppException

class BaseService(ABC):
    """Abstract base service providing common CRUD methods"""

    @classmethod
    @abstractmethod
    def create(cls, data):
        """Create a new record"""
        pass

    @classmethod
    @abstractmethod
    def update(cls, instance, data):
        """Update an existing record"""
        pass

    @classmethod
    def delete(cls, instance):
        """Delete a record"""
        try:
            db.session.delete(instance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise AppException(f"Failed to delete: {str(e)}")
