from sqlalchemy import Column, Integer, String
from app.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    deadline = Column(String)
    status = Column(String, default="Pending")