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
4. Provision AWS resources for Kinesis, Firehose, Glue, and S3.
5. Run the service locally from VS Code for validation.
6. Deploy the same service to EC2.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
Copy-Item .env.example .env
python -m drify_ingestor.main
```

## AWS resource setup

The repository now includes a starter CloudFormation stack at `infra/firehose_parquet_stack.yaml`.

1. Deploy the stack:

```powershell
aws cloudformation deploy `
  --template-file infra/firehose_parquet_stack.yaml `
  --stack-name drify-market-data `
  --capabilities CAPABILITY_NAMED_IAM `
  --parameter-overrides ProjectName=drify EnvironmentName=prod
```

2. Collect the output values for:
   - `KinesisStreamName`
   - `S3BucketName`
   - `FirehoseDeliveryStreamName`
3. Put the `KinesisStreamName` and AWS region into `.env` on your EC2 instance.
4. Attach an IAM role to EC2 that can call `kinesis:PutRecord` on the created stream.
5. After the app starts publishing JSON into Kinesis Data Streams, Firehose will read the stream and land Parquet files under `s3://<bucket>/ticks/...`.

## EC2 runtime setup

On the EC2 box, keep the application environment very close to local:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python -m drify_ingestor.main
```

If you are using Amazon Linux instead of Windows on EC2, the activate command becomes:

```bash
source .venv/bin/activate
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

- Verify records are visible in the Kinesis stream metrics
- Confirm Firehose is writing Parquet files into the S3 `ticks/` prefix
- Add Athena or Glue crawlers for downstream querying if needed
