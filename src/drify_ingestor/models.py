from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta, timezone
from typing import Any


IST = timezone(timedelta(hours=5, minutes=30))


@dataclass(frozen=True)
class TickEvent:
    event_time: str
    instrument: str
    instrument_token: int
    ltp: float
    exchange_timestamp: str | None
    ingestion_time: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_tick_event(tick: dict[str, Any], instrument_name: str = "NIFTY") -> TickEvent:
    exchange_timestamp = _to_iso8601(tick.get("exchange_timestamp"))
    ingestion_time = _utc_now()
    event_time = exchange_timestamp if exchange_timestamp else ingestion_time

    return TickEvent(
        event_time=event_time,
        instrument=instrument_name,
        instrument_token=int(tick["instrument_token"]),
        ltp=float(tick["last_price"]),
        exchange_timestamp=exchange_timestamp,
        ingestion_time=ingestion_time,
    )

def _to_iso8601(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(IST).isoformat()
    return str(value)


def _utc_now() -> str:
    return datetime.now(tz=IST).isoformat()
