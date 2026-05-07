from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Session_Circuit(Base):
    __tablename__ = "session_circuit"

    session_id = Column(Integer, ForeignKey("sessions.session_id"), primary_key=True)
    circuit_name = Column(String, ForeignKey("circuits.circuit_name"), primary_key=True)