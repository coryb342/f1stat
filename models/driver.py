from sqlalchemy import Column, String
from db import Base

class Driver(Base):
    __tablename__ = "drivers"

    driver_code = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)