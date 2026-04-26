from ninja.errors import HttpError

def is_admin(user):
    if user.role != 'admin':
        raise HttpError(403, "Akses ditolak: Anda bukan Admin")
    return True

def is_instructor(user):
    if user.role not in ['instructor', 'admin']:
        raise HttpError(403, "Akses ditolak: Anda bukan Instructor")
    return True

def is_student(user):
    if user.role not in ['student', 'admin']:
        raise HttpError(403, "Akses ditolak: Anda bukan Student")
    return True