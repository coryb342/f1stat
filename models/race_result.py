from sqlalchemy import Column, Integer, String, ForeignKey
from declarative_base import Base

class Race_Result(Base):
    __tablename__ = "race_results"
    
    session_id = Column(Integer, ForeignKey("sessions.session_id"), primary_key=True)
    driver_code = Column(String, ForeignKey("drivers.driver_code"), primary_key=True)
    position = Column(Integer, nullable=False)
    points_earned = Column(Integer, nullable=False)
    fastest_lap_time = Column(String, nullable=True)