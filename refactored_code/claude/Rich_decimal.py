from typing import Optional


def decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    """
    Convert a file size to a human-readable decimal (SI) representation.

    Uses powers of 1000, where 1000 B = 1 kB, following the SI (decimal)
    convention for byte units (as opposed to binary/IEC units like KiB, MiB).

    Args:
        size: File size in bytes.
        precision: Number of decimal places to display in the result.
        separator: String inserted between the numeric value and the unit.

    Returns:
        A formatted string representing the file size using SI units
        (e.g. "1.5 kB").
    """
    # SI (decimal) unit suffixes, in ascending order of magnitude.
    si_units = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    return _to_str(
        size=size,
        suffixes=si_units,
        base=1000,
        precision=precision,
        separator=separator,
    )