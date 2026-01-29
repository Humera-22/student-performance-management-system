import os

class Config:
    # Database configuration using environment variables
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:humerapostgres123@localhost:5432/student_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key")

    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

