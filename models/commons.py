from datetime import datetime

VALID_CURRENCIES = ["USD", "EUR", "GBP"]


def validate_currency(currency: str) -> str:
    if currency not in VALID_CURRENCIES:
        raise ValueError(f"Invalid currency: {currency}")
    return currency


def validate_timestamp_range(timestamp: str) -> str:
    timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    if timestamp_obj > datetime.now():
        raise ValueError(f"Invalid transaction timestamp, in the future: {timestamp}")
    return timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")