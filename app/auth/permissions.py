"""
PERMISSIONS = {
    "STUDENT_VIEW": "student:view",
    "STUDENT_CREATE": "student:create",
    "STUDENT_UPDATE": "student:update",
    "STUDENT_DELETE": "student:delete",

    "COURSE_VIEW": "course:view",
    "COURSE_CREATE": "course:create",

    "PERFORMANCE_ADD": "performance:add",
    "PERFORMANCE_VIEW": "performance:view",

    "USER_CREATE": "user:create",
    "VIEW_EXTERNAL_INFO": "view:external_info",
}

ROLE_PERMISSION_MAP = {
    "admin": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["STUDENT_CREATE"],
        PERMISSIONS["STUDENT_UPDATE"],
        PERMISSIONS["STUDENT_DELETE"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["COURSE_CREATE"],
        PERMISSIONS["PERFORMANCE_ADD"],
        PERMISSIONS["PERFORMANCE_VIEW"],
        PERMISSIONS["USER_CREATE"],
        PERMISSIONS["VIEW_EXTERNAL_INFO"],
    ],
    "principal": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["STUDENT_CREATE"],
        PERMISSIONS["STUDENT_UPDATE"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["COURSE_CREATE"],
        PERMISSIONS["PERFORMANCE_VIEW"],
    ],
    "teacher": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["PERFORMANCE_ADD"],
        PERMISSIONS["PERFORMANCE_VIEW"],
    ],
    "student": [
        PERMISSIONS["STUDENT_UPDATE"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["PERFORMANCE_VIEW"],
    ],
}
"""
# app/auth/permissions.py

# -------------------------
# PERMISSIONS
# -------------------------
PERMISSIONS = {
    # Student permissions
    "STUDENT_VIEW": "student:view",
    "STUDENT_CREATE": "student:create",
    "STUDENT_UPDATE": "student:update",
    "STUDENT_DELETE": "student:delete",

    # Course permissions
    "COURSE_VIEW": "course:view",
    "COURSE_CREATE": "course:create",

    # Performance permissions
    "PERFORMANCE_VIEW": "performance:view",
    "PERFORMANCE_ADD": "performance:add",

    # User management
    "USER_CREATE": "user:create",

    # External API
    "VIEW_EXTERNAL_INFO": "view:external_info",
}

# -------------------------
# ROLE → PERMISSIONS mapping
# -------------------------
ROLE_PERMISSION_MAP = {
    "admin": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["STUDENT_CREATE"],
        PERMISSIONS["STUDENT_UPDATE"],
        PERMISSIONS["STUDENT_DELETE"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["COURSE_CREATE"],
        PERMISSIONS["PERFORMANCE_VIEW"],
        PERMISSIONS["PERFORMANCE_ADD"],
        PERMISSIONS["USER_CREATE"],
        PERMISSIONS["VIEW_EXTERNAL_INFO"],
    ],
    "principal": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["STUDENT_CREATE"],
        PERMISSIONS["STUDENT_UPDATE"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["COURSE_CREATE"],
        PERMISSIONS["PERFORMANCE_VIEW"],
    ],
    "teacher": [
        PERMISSIONS["STUDENT_VIEW"],
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["PERFORMANCE_VIEW"],
        PERMISSIONS["PERFORMANCE_ADD"],
    ],
    "student": [
        PERMISSIONS["STUDENT_UPDATE"],  # student can update only self info
        PERMISSIONS["COURSE_VIEW"],
        PERMISSIONS["PERFORMANCE_VIEW"],
    ],
}
