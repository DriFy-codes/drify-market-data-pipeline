from __future__ import annotations

import logging

from drify_ingestor.config import Settings
from drify_ingestor.kinesis import KinesisPublisher
from drify_ingestor.kite_client import KiteLtpStreamer
from drify_ingestor.logging_config import configure_logging
from drify_ingestor.models import build_tick_event


LOGGER = logging.getLogger(__name__)


def main() -> None:
    settings = Settings.from_env()
    configure_logging(settings.log_level)
    publisher = KinesisPublisher(
        stream_name=settings.kinesis_stream_name,
        region_name=settings.aws_region,
    )

    def handle_tick(tick: dict) -> None:
        if "last_price" not in tick:
            LOGGER.debug("Skipping tick without last_price: %s", tick)
            return

        event = build_tick_event(tick)
        publisher.publish(
            record=event.to_dict(),
            partition_key=settings.kinesis_partition_key,
        )
        LOGGER.info(
            "Published tick timestamp=%s ltp=%s stream=%s",
            event.event_time,
            event.ltp,
            settings.kinesis_stream_name,
        )

    streamer = KiteLtpStreamer(
        api_key=settings.kite_api_key,
        access_token=settings.kite_access_token,
        instrument_token=settings.kite_instrument_token,
        mode=settings.kite_mode,
        tick_handler=handle_tick,
    )
    streamer.connect()


if __name__ == "__main__":
    main()
