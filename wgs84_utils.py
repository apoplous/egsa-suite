"""Utilities for WGS84 input/output used by the EGSA Suite GUI.

The module is deliberately independent from Tkinter so the parsing/formatting
logic can be regression-tested without opening the application UI.
"""

from dataclasses import dataclass
import re
from typing import List, Tuple


@dataclass(frozen=True)
class WGS84Point:
    name: str
    latitude: float
    longitude: float


_DECIMAL_PAIR_RE = re.compile(
    r"^(?P<prefix>.*?)"
    r"(?P<lat>[+-]?\d{1,2}(?:[\.,]\d+)?)"
    r"\s*(?:,\s*|;\s*|\s+)"
    r"(?P<lon>[+-]?\d{1,3}(?:[\.,]\d+)?)\s*$"
)

_DMS_COORD_RE = re.compile(
    r"(?P<deg>[+-]?\d{1,3}(?:[\.,]\d+)?)\s*[°º]\s*"
    r"(?P<minute>\d{1,2}(?:[\.,]\d+)?)\s*['′’]\s*"
    r"(?:(?P<second>\d{1,2}(?:[\.,]\d+)?)\s*[\"″”]\s*)?"
    r"(?P<hem>[NSEW])",
    re.IGNORECASE,
)


def _number(text: str) -> float:
    return float(text.replace(",", "."))


def _safe_name(text: str, fallback: str) -> str:
    cleaned = re.sub(r"[\s,;]+", "_", text.strip())
    return cleaned.strip("_") or fallback


def _validate_lat_lon(latitude: float, longitude: float) -> None:
    if not -90.0 <= latitude <= 90.0:
        raise ValueError(f"latitude εκτός ορίων: {latitude}")
    if not -180.0 <= longitude <= 180.0:
        raise ValueError(f"longitude εκτός ορίων: {longitude}")


def dms_components_to_decimal(degrees, minutes, seconds, hemisphere: str, axis: str) -> float:
    """Convert numeric DMS fields to decimal degrees with strict validation."""
    if axis not in ("lat", "lon"):
        raise ValueError("axis must be lat or lon")

    try:
        deg = _number(str(degrees).strip())
        minute = _number(str(minutes).strip())
        second = _number(str(seconds).strip())
    except (TypeError, ValueError):
        raise ValueError("μοίρες, λεπτά και δευτερόλεπτα πρέπει να είναι αριθμοί")

    hem = str(hemisphere).strip().upper()
    allowed = ("N", "S") if axis == "lat" else ("E", "W")
    if hem not in allowed:
        shown = hem if hem else "—"
        raise ValueError(f"μη έγκυρη διεύθυνση {shown} για {axis}")

    if deg < 0:
        raise ValueError("οι μοίρες γράφονται χωρίς πρόσημο· χρησιμοποίησε N/S/E/W")
    if not 0 <= minute < 60:
        raise ValueError("τα λεπτά πρέπει να είναι από 0 έως <60")
    if not 0 <= second < 60:
        raise ValueError("τα δευτερόλεπτα πρέπει να είναι από 0 έως <60")

    max_deg = 90.0 if axis == "lat" else 180.0
    if deg > max_deg or (deg == max_deg and (minute != 0 or second != 0)):
        raise ValueError(f"οι μοίρες {axis} είναι εκτός ορίων")

    value = deg + minute / 60.0 + second / 3600.0
    if hem in ("S", "W"):
        value = -value
    return value

def parse_dms_coordinate(text: str) -> Tuple[float, str]:
    """Parse one DMS coordinate and return (decimal_degrees, hemisphere)."""
    match = _DMS_COORD_RE.fullmatch(text.strip())
    if not match:
        raise ValueError(f"μη έγκυρη μορφή μοιρών: {text}")

    degrees = _number(match.group("deg"))
    minutes = _number(match.group("minute"))
    seconds = _number(match.group("second") or "0")
    hemisphere = match.group("hem").upper()

    if not 0 <= minutes < 60:
        raise ValueError("τα λεπτά πρέπει να είναι από 0 έως <60")
    if not 0 <= seconds < 60:
        raise ValueError("τα δευτερόλεπτα πρέπει να είναι από 0 έως <60")

    value = abs(degrees) + minutes / 60.0 + seconds / 3600.0
    if hemisphere in ("S", "W"):
        value = -value
    elif degrees < 0:
        raise ValueError("αρνητικές μοίρες με N/E δεν είναι έγκυρος συνδυασμός")

    return value, hemisphere


def format_wgs84_dms(value: float, axis: str) -> str:
    """Format decimal WGS84 latitude/longitude as compact DMS."""
    if axis not in ("lat", "lon"):
        raise ValueError("axis must be 'lat' or 'lon'")

    limit = 90.0 if axis == "lat" else 180.0
    if not -limit <= value <= limit:
        raise ValueError("coordinate εκτός ορίων")

    hemisphere = ("N" if value >= 0 else "S") if axis == "lat" else ("E" if value >= 0 else "W")
    total_seconds = round(abs(value) * 3600.0, 3)
    degrees = int(total_seconds // 3600)
    remainder = total_seconds - degrees * 3600
    minutes = int(remainder // 60)
    seconds = remainder - minutes * 60

    # Handle the rare rounding case 59.9995 -> 60.000.
    if seconds >= 59.9995:
        seconds = 0.0
        minutes += 1
    if minutes >= 60:
        minutes = 0
        degrees += 1

    return f"{degrees}°{minutes:02d}′{seconds:06.3f}″{hemisphere}"


def parse_wgs84_points(text: str, format_name: str = "decimal") -> Tuple[List[WGS84Point], List[str]]:
    """Parse one WGS84 point per line.

    decimal:
        A 40.27212345 22.50345678
        A 40.27212345, 22.50345678
        A 40,27212345 22,50345678

    dms:
        A 40°16′19.644″N 22°30′12.444″E

    Decimal input order is explicitly Latitude, Longitude. DMS input can be
    supplied in either order because N/S and E/W identify each axis.
    """
    mode = format_name.strip().lower()
    if mode not in ("decimal", "dms"):
        raise ValueError("format_name must be 'decimal' or 'dms'")

    points: List[WGS84Point] = []
    errors: List[str] = []
    auto_index = 0

    for line_num, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue

        try:
            fallback = chr(ord("A") + auto_index) if auto_index < 26 else f"P{auto_index + 1}"

            if mode == "decimal":
                match = _DECIMAL_PAIR_RE.match(line)
                if not match:
                    raise ValueError("αναμένεται: Όνομα Latitude Longitude")
                latitude = _number(match.group("lat"))
                longitude = _number(match.group("lon"))
                name = _safe_name(match.group("prefix"), fallback)
            else:
                matches = list(_DMS_COORD_RE.finditer(line))
                if len(matches) != 2:
                    raise ValueError("αναμένονται δύο συντεταγμένες DMS με N/S και E/W")

                first_start = matches[0].start()
                name = _safe_name(line[:first_start], fallback)
                latitude = None
                longitude = None
                for match in matches:
                    value, hemisphere = parse_dms_coordinate(match.group(0))
                    if hemisphere in ("N", "S"):
                        if latitude is not None:
                            raise ValueError("βρέθηκαν δύο latitude")
                        latitude = value
                    else:
                        if longitude is not None:
                            raise ValueError("βρέθηκαν δύο longitude")
                        longitude = value
                if latitude is None or longitude is None:
                    raise ValueError("απαιτούνται μία latitude (N/S) και μία longitude (E/W)")

            _validate_lat_lon(latitude, longitude)
            points.append(WGS84Point(name=name, latitude=latitude, longitude=longitude))
            auto_index += 1
        except ValueError as exc:
            errors.append(f"Γραμμή {line_num}: {exc}")

    return points, errors
