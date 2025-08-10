# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LogLine(Base):
    __tablename__ = 'log_lines'

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, index=True)
    timestamp = Column(DateTime, nullable=True)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)