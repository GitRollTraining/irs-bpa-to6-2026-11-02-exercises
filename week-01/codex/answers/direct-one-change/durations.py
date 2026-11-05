"""Parse short durations such as "1h30m" into seconds."""
import re

PART = re.compile(r"(\d+)([dhms])")  # one number and its unit
SECONDS = {"d": 86400, "h": 3600, "m": 60, "s": 1}  # seconds in one of each unit


def parse_duration(text: str) -> int:
    """Return the number of seconds in a duration written as numbers with units, with no spaces.

    The units are d (days), h (hours), m (minutes) and s (seconds), as in "2d", "1h30m", "45s" or "2h5s".

    Args:
        text: The duration, for example "1h30m".

    Returns:
        The duration in seconds, for example 5400 for "1h30m".

    Raises:
        ValueError: If the text is empty, or holds anything other than numbers with the units d, h, m and s.
    """
    text = text.strip()
    if not text or PART.sub("", text):  # empty, or text left over that is not a number with its unit
        raise ValueError(f"not a duration: {text!r}")
    return sum(int(number) * SECONDS[unit] for number, unit in PART.findall(text))
