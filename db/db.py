
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Use DATABASE_URL if available (Railway), otherwise build from individual vars (local)
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Local development: Build URL from individual environment variables
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
                       DATABASE_URL,
                       connect_args={"connect_timeout": 10},
                       pool_pre_ping=True,
                       pool_recycle=3600,
    
    
    
    
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()