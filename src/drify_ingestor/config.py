from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    kite_api_key: str
    kite_access_token: str
    aws_region: str
    kinesis_stream_name: str
    kinesis_partition_key: str
    kite_instrument_token: int
    kite_mode: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            kite_api_key=_get_required("KITE_API_KEY"),
            kite_access_token=_get_required("KITE_ACCESS_TOKEN"),
            aws_region=_get_required("AWS_REGION"),
            kinesis_stream_name=_get_required("KINESIS_STREAM_NAME"),
            kinesis_partition_key=os.getenv("KINESIS_PARTITION_KEY", "NIFTY"),
            kite_instrument_token=int(os.getenv("KITE_INSTRUMENT_TOKEN", "256265")),
            kite_mode=os.getenv("KITE_MODE", "ltp"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


def _get_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value
