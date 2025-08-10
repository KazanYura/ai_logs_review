from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from app.core.logging_config import ANONYMIZATION_PATTERNS, LOG_LINE_REGEX
from app.models.log import LogEntry
from app.db.base import init_db
from app.db.crud import create_log, save_log_line

class LogProcessor:
    def __init__(self):
        pass

    async def process_log_text(self, text: str) -> list[LogEntry]:
        lines = text.splitlines()
        processed_entries = []

        for line in lines:
            entry = self._process_log_line(line)
            if entry is not None:
                processed_entries.append(entry)
        log_id = await create_log()
        for entry in processed_entries:
            await save_log_line(log_id, entry)
        return processed_entries


    def _anonymize_log(self, text: str) -> str:
        for key, pattern in ANONYMIZATION_PATTERNS.items():
            text = pattern.sub(f'[{key}]', text)
        return text

    def _parse_log_line(self, line: str) -> Optional[LogEntry]:
        match = LOG_LINE_REGEX.match(line)
        if not match:
            return None

        timestamp_str = match.group('timestamp')
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            timestamp = None

        try:
            log_entry = LogEntry(
                timestamp=timestamp,
                level=match.group('level'),
                message=match.group('message')
            )
        except ValidationError:
            return None

        return log_entry

    def _process_log_line(self, line: str) -> Optional[LogEntry]:
        log_entry = self._parse_log_line(line)
        if not log_entry:
            return None
        log_entry.message = self._anonymize_log(log_entry.message)
        return log_entry

