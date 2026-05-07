from sqlalchemy import Column, String
from db import Base

class Constructor(Base):
    __tablename__ = "constructors"

    name = Column(String, primary_key=True)
    nationality = Column(String, nullable=False)


    