from __future__ import annotations

import json
import logging
from typing import Any

import boto3


LOGGER = logging.getLogger(__name__)


class KinesisPublisher:
    def __init__(self, stream_name: str, region_name: str) -> None:
        self.stream_name = stream_name
        self.client = boto3.client("kinesis", region_name=region_name)

    def publish(self, record: dict[str, Any], partition_key: str) -> dict[str, Any]:
        payload = json.dumps(record).encode("utf-8")
        response = self.client.put_record(
            StreamName=self.stream_name,
            Data=payload,
            PartitionKey=partition_key,
        )
        LOGGER.debug(
            "Published record to Kinesis stream=%s shard=%s sequence=%s",
            self.stream_name,
            response.get("ShardId"),
            response.get("SequenceNumber"),
        )
        return response

