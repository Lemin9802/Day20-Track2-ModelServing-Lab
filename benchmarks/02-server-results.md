# 02 — Server Results

## Smoke Test

See:

- `benchmarks/02-server-smoke.md`

The local server returned a valid OpenAI-compatible chat completion response with:

- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- Response content: `OK`

## Metrics

See:

- `benchmarks/02-server-metrics.md`

The native `llama-server` exposed Prometheus-compatible metrics at:

- `http://127.0.0.1:8080/metrics`

Observed metrics after one request included:

- `llamacpp:prompt_tokens_total 36`
- `llamacpp:tokens_predicted_total 2`
- `llamacpp:prompt_tokens_seconds 25.9179`
- `llamacpp:predicted_tokens_seconds 55.5556`

## Load Test

See:

- `benchmarks/02-load-test-summary.md`
- `benchmarks/02-locust-10_stats.csv`
- `benchmarks/02-locust-50_stats.csv`

### Summary

| Concurrency | Total requests | Failures | Average latency | P50 | P95 | P99 | Throughput |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 28 | 0 | 15.5s | 18s | 22s | 23s | 0.48 req/s |
| 50 | 16 | 0 | 30.1s | 31s | 53s | 53s | 0.29 req/s |

## Observation

The server stayed stable with zero failed requests at both 10 and 50 concurrent users. Latency increased at 50 users because the local server was configured with 2 parallel slots, so most requests waited in queue.
