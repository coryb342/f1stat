from sqlalchemy import Column, ForeignKey, String
from db import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    favorite_driver = Column(String, ForeignKey("drivers.driver_code"))
    password = Column(String, nullable=False)