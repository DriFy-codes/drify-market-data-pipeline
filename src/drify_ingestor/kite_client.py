from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from kiteconnect import KiteTicker


LOGGER = logging.getLogger(__name__)


TickHandler = Callable[[dict[str, Any]], None]


class KiteLtpStreamer:
    def __init__(
        self,
        api_key: str,
        access_token: str,
        instrument_token: int,
        mode: str,
        tick_handler: TickHandler,
    ) -> None:
        self.instrument_token = instrument_token
        self.mode = mode
        self.tick_handler = tick_handler
        self.ticker = KiteTicker(api_key, access_token)

        self.ticker.on_ticks = self._on_ticks
        self.ticker.on_connect = self._on_connect
        self.ticker.on_close = self._on_close
        self.ticker.on_error = self._on_error
        self.ticker.on_reconnect = self._on_reconnect
        self.ticker.on_noreconnect = self._on_noreconnect

    def connect(self) -> None:
        LOGGER.info("Connecting to Kite WebSocket for instrument_token=%s", self.instrument_token)
        self.ticker.connect(threaded=False)

    def _on_connect(self, ws: Any, response: Any) -> None:
        LOGGER.info("Connected to Kite WebSocket, subscribing to %s", self.instrument_token)
        ws.subscribe([self.instrument_token])
        ws.set_mode(self.mode, [self.instrument_token])

    def _on_ticks(self, ws: Any, ticks: list[dict[str, Any]]) -> None:
        for tick in ticks:
            if tick.get("instrument_token") != self.instrument_token:
                continue
            self.tick_handler(tick)

    def _on_close(self, ws: Any, code: int, reason: str) -> None:
        LOGGER.warning("Kite WebSocket closed code=%s reason=%s", code, reason)

    def _on_error(self, ws: Any, code: int, reason: str) -> None:
        LOGGER.exception("Kite WebSocket error code=%s reason=%s", code, reason)

    def _on_reconnect(self, ws: Any, attempts_count: int) -> None:
        LOGGER.warning("Reconnecting to Kite WebSocket attempt=%s", attempts_count)

    def _on_noreconnect(self, ws: Any) -> None:
        LOGGER.error("Kite WebSocket stopped reconnecting")

