from sqlalchemy import Column, String
from declarative_base import Base

class Circuit(Base):
    __tablename__ = "circuits"

    circuit_name = Column(String, primary_key=True)
    location = Column(String, nullable=False)
    country = Column(String, nullable=False)