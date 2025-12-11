from datetime import datetime


def validate_timestamp_range(timestamp: str) -> str:
    timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    if timestamp_obj > datetime.now():
        raise ValueError(f"Invalid transaction timestamp, in the future: {timestamp}")
    return timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")