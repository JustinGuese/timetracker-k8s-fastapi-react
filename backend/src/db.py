from datetime import date, datetime, timedelta
from enum import Enum
from os import environ
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = "postgresql+psycopg2://" + environ["PSQL_URL"] # user:password@postgresserver/db

engine = create_engine(DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class TimeEntryDB(Base):
    __tablename__ = "timesheets"
    start_time = Column(DateTime, primary_key=True, unique=True, nullable=False)
    end_time = Column(DateTime, nullable=False)
    customer = Column(String, nullable=False)
    duration_hours = Column(Float, nullable=False)
    
## pydantic

class TimerStart(BaseModel):
    customer: str
    start_time: datetime
    
class TimerEnd(BaseModel):
    customer: str
    end_time: datetime
    
class TimeEntryInfo(BaseModel):
    customer: str
    running: bool
    start_time: Optional[datetime]
    
Base.metadata.create_all(engine)