from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Qualifying_Result(Base):
    __tablename__ = "qualifying_results"
    
    session_id = Column(Integer, ForeignKey("sessions.session_id"), primary_key=True)
    driver_code = Column(String, ForeignKey("drivers.driver_code"), primary_key=True)
    position = Column(Integer, nullable=False)
    Q1_time = Column(String, nullable=True)
    Q2_time = Column(String, nullable=True)
    Q3_time = Column(String, nullable=True)