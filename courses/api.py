from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from .schemas import CourseSchema, CourseCreateSchema
from .models import Course
from .models import Lesson

@api_controller("/lessons", auth=JWTAuth())
class LessonController:
    
    @http_get("/", response=list[LessonSchema])
    def list_lessons(self, course_id: int = None):
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()

    @http_post("/", response=LessonSchema)
    def create_lesson(self, data: LessonCreateSchema):
        return Lesson.objects.create(**data.dict())

# 1. Definisi Controller
@api_controller("/courses", auth=JWTAuth())
class CourseController:
    
    @http_get("/", response=list[CourseSchema])
    def list_courses(self):
        return Course.objects.for_listing().all()

    @http_post("/", response=CourseSchema)
    def create_course(self, data: CourseCreateSchema):
        return Course.objects.create(
            title=data.title,
            category_id=data.category_id,
            instructor=self.context.request.user
        )

# 2. Inisialisasi API
api = NinjaExtraAPI(auth=JWTAuth())

# 3. DAFTARKAN KEDUANYA DI SINI
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(CourseController)
# ... (tambahkan di baris registrasi bawah)
api.register_controllers(LessonController)