from datetime import datetime


def parse_timestamp(timestamp_str: str) -> datetime:
    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    if not timestamp.tzinfo:
        raise AssertionError(f'no tzinfo found for {repr(timestamp_str)}')
    return timestamp
