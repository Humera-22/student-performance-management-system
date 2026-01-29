# app/dataclasses.py
from dataclasses import dataclass

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
