from sqlalchemy import Column, Integer, String
from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    quiz_name = Column(String)
    score = Column(Integer)