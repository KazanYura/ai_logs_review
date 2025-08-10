import re

ANONYMIZATION_PATTERNS = {
    'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    'FILENAME': re.compile(r'\b[\w,\s-]+\.(txt|log|csv|json|xml|py|exe|docx?|xlsx?)\b', re.IGNORECASE),
    'IP': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    'TOKEN': re.compile(r'\b(?:token|apikey|api_key|access_token|secret)[=: ]+[A-Za-z0-9\-_.]{10,}\b', re.IGNORECASE),
}


LOG_LINE_REGEX = re.compile(
    r'^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3,6})\]\s+'
    r'\[(?P<level>[A-Z]+)\]\s+'
    r'(?P<message>.*)$'
)