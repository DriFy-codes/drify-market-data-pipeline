# DriFy Market Data Pipeline

This repository contains the MVP ingestion service for streaming one instrument from KiteConnect into AWS.

## MVP scope

- Subscribe to one instrument only
- Capture only `NIFTY` LTP ticks
- Publish normalized tick events to `Amazon Kinesis Data Streams`
- Let `Kinesis Data Firehose` deliver the data into `S3` as `Parquet`

## Suggested project flow

1. Create a Python virtual environment.
2. Install the project in editable mode.
3. Copy `.env.example` to `.env` and fill in KiteConnect and AWS values.
4. Run the service locally from VS Code.
5. After validation, deploy the same service to EC2.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
Copy-Item .env.example .env
python -m drify_ingestor.main
```

## Environment variables

- `KITE_API_KEY`: Zerodha Kite API key
- `KITE_ACCESS_TOKEN`: Zerodha access token for the logged-in session
- `AWS_REGION`: AWS region where the Kinesis stream exists
- `KINESIS_STREAM_NAME`: Kinesis Data Stream name
- `KINESIS_PARTITION_KEY`: Partition key used while publishing records
- `KITE_INSTRUMENT_TOKEN`: Instrument token to subscribe to for the MVP
- `KITE_MODE`: WebSocket mode, keep this as `ltp` for MVP
- `LOG_LEVEL`: Python log level

## Normalized record schema

Each tick is converted into a compact JSON event before being pushed to Kinesis:

```json
{
  "event_time": "2026-04-15T09:45:10.123000+00:00",
  "instrument": "NIFTY",
  "instrument_token": 256265,
  "ltp": 22456.75,
  "exchange_timestamp": "2026-04-15T09:45:10+00:00",
  "ingestion_time": "2026-04-15T09:45:10.456000+00:00"
}
```

## Recommended next steps

- Create the AWS resources: `Kinesis Data Stream`, `Firehose`, and `S3`
- Add a Glue catalog table once files begin landing in S3
- Package and deploy this service on EC2

