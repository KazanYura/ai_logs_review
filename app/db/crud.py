# app/db/crud.py

from sqlalchemy.future import select # <-- Add this import
from app.db.models import LogLine, Log
from app.db.base import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import LogEntry


async def save_log_line(log_id: int, entry: LogEntry):
    async with AsyncSessionLocal() as session:
        log_line = LogLine(
            log_id=log_id,
            timestamp=entry.timestamp,
            level=entry.level,
            message=entry.message,
        )
        session.add(log_line)
        await session.commit()
        await session.refresh(log_line)
        return log_line.id


async def create_log():
    async with AsyncSessionLocal() as session:
        log = Log()
        session.add(log)
        await session.commit()
        await session.refresh(log)
        return log.id


async def get_log_lines_by_id(log_id: int) -> list[LogLine]:
    async with AsyncSessionLocal() as session:
        query = select(LogLine).where(LogLine.log_id == log_id)
        result = await session.execute(query)
    return result.scalars().all()