# 📚 Simple LMS - Django Database & ORM Optimization

Project ini adalah implementasi **Data Models** untuk sistem Learning Management System (LMS) sederhana menggunakan Django ORM, PostgreSQL, dan Docker. Fokus utama project ini adalah desain skema database yang efisien dan optimasi query untuk menghindari masalah N+1.

---

## 🎯 Learning Objectives Achieved
- [x] Desain Database Schema LMS dengan relasi kompleks.
- [x] Implementasi Custom User Model dengan Role Management.
- [x] Optimasi Query menggunakan `select_related` dan `prefetch_related`.
- [x] Kustomisasi Django Admin Interface (Inlines, Filters, Search).

---

## 🏗️ Database Architecture
Aplikasi ini terdiri dari beberapa model utama dengan relasi sebagai berikut:
- **User**: Custom model dengan role `admin`, `instructor`, dan `student`.
- **Category**: Menggunakan *self-referencing ForeignKey* untuk mendukung hierarki kategori (Induk & Sub-kategori).
- **Course**: Terhubung ke Instructor dan Category.
- **Lesson**: Memiliki fitur *ordering* untuk menentukan urutan materi.
- **Enrollment**: Menghubungkan Student ke Course dengan *Unique Constraint*.
- **Progress**: Melacak status penyelesaian materi oleh student.

---

## ⚡ Query Optimization (N+1 Problem Solution)
Salah satu poin utama dalam tugas ini adalah optimasi query. Kami menggunakan **Model Managers** kustom untuk membungkus logika optimasi:

### Contoh Perbandingan:
**Tanpa Optimasi (Bad Practice):**
```python
# Ini akan memicu 1 query untuk Course + N query untuk setiap Instructor
courses = Course.objects.all()
for c in courses:
    print(c.instructor.username)

🖼️ Dokumentasi Implementasi (Screenshots)

1. Django Admin Dashboard
images/admindjango.png
Menampilkan menu untuk User, Courses, Categories, dan Enrollment.

2. Course Management (Inlines)
images/course-management.png
Menunjukkan fitur penambahan Lesson secara langsung di dalam halaman Course menggunakan TabularInline.

3. Database Migrations
images/migration.png
Bukti bahwa migrasi telah berhasil diterapkan ke PostgreSQL.