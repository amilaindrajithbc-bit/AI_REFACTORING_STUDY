from typing import Optional

def decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    """
    Convert a file size in bytes to a human-readable decimal (SI) string.

    Uses decimal (base-1000) units such as kB, MB, GB, and TB.

    Args:
        size: File size in bytes.
        precision: Number of decimal places to display.
        separator: Separator between the numeric value and the unit.

    Returns:
        A formatted string representing the file size using SI units.
    """
    suffixes = (
        "kB",
        "MB",
        "GB",
        "TB",
        "PB",
        "EB",
        "ZB",
        "YB",
    )

    return _to_str(
        size=size,
        suffixes=suffixes,
        base=1000,
        precision=precision,
        separator=separator,
    )