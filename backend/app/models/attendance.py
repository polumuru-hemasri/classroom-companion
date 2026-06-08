from sqlalchemy import Column, Integer, String
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    date = Column(String)
    status = Column(String)