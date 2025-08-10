from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class LogEntry(BaseModel):
    timestamp: Optional[datetime]
    level: str
    message: str

    @validator('level')
    def validate_level(cls, v):
        allowed_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if v not in allowed_levels:
            raise ValueError(f'Invalid log level: {v}')
        return v
