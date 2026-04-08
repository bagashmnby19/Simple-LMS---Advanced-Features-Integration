from django.db import models
from django.contrib.auth.models import AbstractUser

# --- CUSTOM QUERYSET & MANAGER (Letakkan di atas agar bisa dipakai di Class Course) ---

class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        # Optimasi N+1: Mengambil data instructor & category sekaligus dalam 1 query SQL JOIN
        return self.select_related('instructor', 'category')

class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self, student):
        # Optimasi: Mengambil data course sekaligus untuk dashboard student
        return self.filter(student=student).select_related('course')


# --- MODELS ---

# 1. Custom User Model
class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='student')

# 2. Category Model (Self-referencing)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# 3. Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    # Menghubungkan Manager Custom
    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return self.title

# 4. Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# 5. Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        unique_together = ('student', 'course')

# 6. Progress Model
class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Progress"