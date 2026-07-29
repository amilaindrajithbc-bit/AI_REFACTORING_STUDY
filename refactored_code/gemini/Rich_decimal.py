from typing import Optional


def decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    """Convert a file size in bytes to a human-readable decimal (SI) representation.

    Uses powers of 1000 (e.g., 1000 B = 1 kB).

    Args:
        size: File size in bytes to convert.
        precision: Number of decimal places to display. Defaults to 1.
        separator: String inserted between the numeric value and the unit.
            Defaults to " ".

    Returns:
        A formatted string representing the file size using standard SI units.
    """
    si_units = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    return _to_str(
        size=size,
        suffixes=si_units,
        base=1000,
        precision=precision,
        separator=separator,
    )