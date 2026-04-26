from ninja import Schema
from typing import List, Optional

class CategorySchema(Schema):
    id: int
    name: str

class CourseSchema(Schema):
    id: int
    title: str
    category: CategorySchema
    instructor_id: int

class CourseCreateSchema(Schema):
    title: str
    category_id: int

class LessonCreateSchema(Schema):
    course_id: int
    title: str
    content: str
    order: int

class LessonSchema(Schema):
    id: int
    title: str
    content: str
    order: int
    course_id: int