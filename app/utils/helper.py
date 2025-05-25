from datetime import datetime, timezone

def utcnow_naive():
    """Returns the current UTC time as a naive datetime object.
    This function is used to ensure that the datetime objects stored in the database
    do not include timezone information, which is important for compatibility with
    certain database configurations and libraries.
    Returns:
        datetime: The current UTC time as a naive datetime object.
    """
    return datetime.now(timezone.utc)
    