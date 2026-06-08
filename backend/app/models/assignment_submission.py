from sqlalchemy import Column, Integer, String
from app.database import Base


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer)
    assignment_id = Column(Integer)

    status = Column(String, default="Pending")

    feedback = Column(String, nullable=True)
    submission_text = Column(
    String,
    nullable=True
)