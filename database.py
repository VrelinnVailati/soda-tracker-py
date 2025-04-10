from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import zoneinfo

SQLALCHEMY_DATABASE_URL = "sqlite:///soda_tracker.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SodaConsumption(Base):
    __tablename__ = "soda_consumption"

    utc_dt = datetime.datetime.now(datetime.timezone.utc)

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=utc_dt)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 