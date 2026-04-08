from django.contrib import admin
from .models import User, Category, Course, Lesson, Enrollment

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'created_at')
    list_filter = ('category', 'instructor')
    search_fields = ('title',)
    inlines = [LessonInline]

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Enrollment)