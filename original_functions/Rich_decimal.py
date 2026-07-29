from typing import Optional

def decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    """
    Convert a file size to a human-readable decimal (SI) representation.

    Uses powers of 1000, where 1000 B = 1 kB.

    Args:
        size: File size in bytes.
        precision: Number of decimal places to display.
        separator: String inserted between the numeric value and the unit.

    Returns:
        A formatted string representing the file size using SI units.
    """
    units = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    return _to_str(
        size=size,
        suffixes=units,
        base=1000,
        precision=precision,
        separator=separator,
    )