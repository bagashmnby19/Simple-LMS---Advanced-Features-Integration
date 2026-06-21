import csv
import os
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Course, Enrollment

User = get_user_model()

@shared_task
def send_enrollment_email(student_email, course_title):
    """Task 1: Mengirim email saat student berhasil enroll"""
    subject = f"Selamat! Kamu Terdaftar di Kursus {course_title}"
    message = f"Halo, kamu berhasil terdaftar di kursus {course_title}. Selamat belajar dan jaga kesehatan!"
    from_email = "noreply@healthylife.com"
    
    # Simulasi pengiriman (akan muncul di log terminal worker atau SMTP jika dikonfigurasi)
    send_mail(subject, message, from_email, [student_email], fail_silently=True)
    return f"Email sent to {student_email}"

@shared_task
def generate_certificate(student_id, course_id):
    """Task 2: Menghasilkan sertifikat saat kursus selesai"""
    try:
        user = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        
        # Simulasi generate sertifikat (bisa menulis file atau simpan log)
        cert_data = f"CERTIFICATE OF COMPLETION\nGiven to: {user.username}\nFor Course: {course.title}"
        return f"Certificate generated successfully for {user.username}"
    except Exception as e:
        return f"Error generating certificate: {str(e)}"

@shared_task
def update_course_statistics():
    """Task 3: Scheduled task untuk update jumlah pendaftar kursus"""
    courses = Course.objects.all()
    updated_count = 0
    for course in courses:
        # Menghitung total pendaftar di PostgreSQL
        enrollment_count = Enrollment.objects.filter(course=course).count()
        # Di sini kamu bisa mengupdate field 'enrollment_count' di model Course jika ada
        updated_count += 1
    return f"Updated statistics for {updated_count} courses"

@shared_task
def export_course_report():
    """Task 4: Generate laporan CSV secara asynchronous"""
    file_path = "/app/course_report.csv"
    courses = Course.objects.all()
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Title', 'Instructor'])
        for course in courses:
            writer.writerow([course.id, course.title, course.instructor.username if course.instructor else 'No Instructor'])
            
    return f"Report exported successfully to {file_path}"