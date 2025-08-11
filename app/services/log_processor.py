# app/services/log_processor.py

from .vector_search import LogVectorStore
from .embedding_service import get_embedding_service
from app.db.crud import create_log, save_log_line
from app.models.log import LogEntry
from app.core.logging_config import LOG_LINE_REGEX, ANONYMIZATION_PATTERNS
from datetime import datetime
from pydantic import ValidationError
from typing import Optional

class LogProcessor:
    def __init__(self):
        self._embedding_service = get_embedding_service()
        self._vector_dim = 384

    async def process_and_index_log_file(self, text: str):
        lines = text.splitlines()
        processed_entries = []
        for line in lines:
            entry = self._process_log_line(line)
            if entry:
                processed_entries.append(entry)

        if not processed_entries:
            return [], None
        
        log_id = await create_log()
        for entry in processed_entries:
            await save_log_line(log_id, entry)

        print(f"Creating vector index for new log_id: {log_id}...")
        vector_store = LogVectorStore(dim=self._vector_dim, log_id=log_id)
        
        log_messages = [entry.message for entry in processed_entries]
        embeddings = self._embedding_service.encode(log_messages)
        
        vector_store.add(embeddings, log_messages)
        vector_store.save()

        return processed_entries, log_id


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

