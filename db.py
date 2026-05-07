import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from dotenv import load_dotenv

Base = declarative_base()

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
def establish_connection():
    try:
        engine = create_engine(DB_URL)
        session = Session(engine)
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return

    return session



