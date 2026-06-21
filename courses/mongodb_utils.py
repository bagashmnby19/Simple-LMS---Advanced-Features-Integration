from django.conf import settings
from datetime import datetime

db = settings.MONGO_DB

def log_activity(user_id, username, action, details):
    """Menyimpan log aktivitas user ke MongoDB"""
    activity_collection = db["activity_logs"]
    log_data = {
        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    activity_collection.insert_one(log_data)

def log_learning_analytics(user_id, course_id, progress_percentage):
    """Menyimpan analitik belajar ke MongoDB"""
    analytics_collection = db["learning_analytics"]
    analytics_data = {
        "user_id": user_id,
        "course_id": course_id,
        "progress_percentage": progress_percentage,
        "updated_at": datetime.utcnow()
    }
    analytics_collection.replace_one(
        {"user_id": user_id, "course_id": course_id}, 
        analytics_data, 
        upsert=True
    )

def get_activity_report():
    """Menggunakan Aggregation Query MongoDB untuk laporan"""
    activity_collection = db["activity_logs"]
    pipeline = [
        {"$group": {"_id": "$action", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(activity_collection.aggregate(pipeline))