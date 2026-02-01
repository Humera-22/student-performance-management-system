import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:humerapostgres123@localhost:5432/student_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
