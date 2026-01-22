class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:humerapostgres123@localhost:5432/student_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "supersecretjwtkey123"
    JWT_ALGORITHM = "HS256"
