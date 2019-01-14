# Labrador

Service to *retrieve* data from sources (databases, APIs and etc.) in an async
mode (maybe using threads, but not necessarily).


## Architecture

Initially I wrote a simple HTTP service, but the goal is to use Kafka (or other
queue system) and a special thread subscribed to a topic creating new threads
for retrieve jobs.


## Running

```bash
export BIGQUERY_CREDENTIALS_BASE64="<CONTENT_OF_CREDENTIALS_FILE_IN_BASE64>"
./start.sh
```
