# app/dataclasses.py
from dataclasses import dataclass

# -------- REQUESTS --------
@dataclass
class StudentRequest:
    name: str
    email: str

@dataclass
class CourseRequest:
    title: str

@dataclass
class PerformanceRequest:
    student_id: int
    course_id: int
    marks: int

@dataclass
class UserRequest:
    username: str
    password: str
    roles: list  # list of roles


# -------- RESPONSES --------
@dataclass
class StudentResponse:
    id: int
    name: str
    email: str

@dataclass
class CourseResponse:
    id: int
    title: str

@dataclass
class PerformanceResponse:
    student_id: int
    course_id: int
    marks: int

@dataclass
class UserResponse:
    id: int
    username: str
    roles: list
