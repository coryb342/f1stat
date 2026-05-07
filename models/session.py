from sqlalchemy import Column, Integer, String, Date
from db import Base

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, unique=True)
    session_type = Column(String, primary_key=True)
    session_date = Column(Date, primary_key=True)
    season = Column(Integer, nullable=False)
    