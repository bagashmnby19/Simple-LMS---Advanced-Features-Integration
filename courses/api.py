from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from .schemas import CourseSchema, CourseCreateSchema, EnrollmentSchema, EnrollmentCreateSchema
from .models import Course, Enrollment
from .tasks import send_enrollment_email, export_course_report
from .mongodb_utils import log_activity, get_activity_report

# Inisialisasi API Utama
api = NinjaExtraAPI(auth=JWTAuth())

@api_controller("/courses", auth=JWTAuth())
class CourseController:

    # Rate limiting: Maksimal 60 request per menit berdasarkan IP user
    @method_decorator(ratelimit(key='ip', rate='60/m', block=True))
    @http_get("/", response=list[CourseSchema])
    def list_courses(self):
        # 1. Cek apakah ada data di dalam Redis Cache
        cache_key = "course_list_data"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        # 2. Jika tidak ada di cache, ambil dari PostgreSQL database
        courses = list(Course.objects.all())
        
        # 3. Simpan hasil ke Redis Cache selama 15 menit (900 detik)
        cache.set(cache_key, courses, timeout=900)
        
        # Log ke MongoDB
        log_activity(self.context.request.user.id, self.context.request.user.username, "VIEW_COURSES", "User viewed course list")
        return courses

    @http_post("/", response=CourseSchema)
    def create_course(self, data: CourseCreateSchema):
        course = Course.objects.create(
            title=data.title, 
            category_id=data.category_id, 
            instructor=self.context.request.user
        )
        
        # Cache Invalidation Strategy: Hapus cache list karena ada data baru
        cache.delete("course_list_data")
        
        # Log ke MongoDB
        log_activity(self.context.request.user.id, self.context.request.user.username, "CREATE_COURSE", f"Created course {course.title}")
        return course

    @http_get("/{course_id}/", response=CourseSchema)
    def get_course_detail(self, course_id: int):
        # Caching untuk detail kursus spesifik
        cache_key = f"course_detail_{course_id}"
        cached_course = cache.get(cache_key)
        
        if cached_course:
            return cached_course
            
        try:
            course = Course.objects.get(id=course_id)
            cache.set(cache_key, course, timeout=900)
            return course
        except Course.DoesNotExist:
            return 404, {"detail": "Course not found"}

@api_controller("/enrollments", auth=JWTAuth())
class EnrollmentController:
    
    @http_post("/", response=EnrollmentSchema)
    def enroll(self, data: EnrollmentCreateSchema):
        enrollment = Enrollment.objects.create(
            student=self.context.request.user,
            course_id=data.course_id
        )
        
        # Memicu Celery Asynchronous Task untuk kirim Email
        send_enrollment_email.delay(self.context.request.user.email, enrollment.course.title)
        
        # Log ke MongoDB
        log_activity(self.context.request.user.id, self.context.request.user.username, "ENROLL_COURSE", f"Enrolled in {enrollment.course.title}")
        
        return {
            "id": enrollment.id,
            "course_title": enrollment.course.title,
            "enrolled_at": str(enrollment.enrolled_at)
        }

@api_controller("/reports", auth=JWTAuth())
class ReportController:
    
    @http_post("/export-csv/")
    def trigger_csv_report(self):
        """Memicu background task Celery untuk export CSV"""
        task = export_course_report.delay()
        return {"status": "Processing", "task_id": task.id}
        
    @http_get("/mongo-activities/")
    def view_mongo_report(self):
        """Mengambil data laporan langsung dari aggregasi MongoDB"""
        return get_activity_report()

# Registrasi seluruh controller ke Django Ninja Extra
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(CourseController)
api.register_controllers(EnrollmentController)
api.register_controllers(ReportController)