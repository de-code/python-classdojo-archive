from datetime import datetime


def parse_timestamp(timestamp_str: str) -> datetime:
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
