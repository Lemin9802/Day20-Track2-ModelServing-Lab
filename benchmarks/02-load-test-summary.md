# 02 — Load Test Summary

## Server Configuration

- Server: native `llama-server`
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- Model: Qwen2.5-7B-Instruct Q4_K_M
- Backend: CUDA
- GPU: NVIDIA RTX 4060 Laptop GPU
- Context size: 2048
- GPU layers: 99
- Threads: 24
- Parallel slots: 2
- Continuous batching: enabled
- Metrics endpoint: enabled

## 10 Concurrent Users

| Metric | Value |
|---|---:|
| Total requests | 28 |
| Failures | 0 |
| Average latency | 15.5s |
| P50 latency | 18s |
| P95 latency | 22s |
| P99 latency | 23s |
| Throughput | 0.48 req/s |

## 50 Concurrent Users

| Metric | Value |
|---|---:|
| Total requests | 16 |
| Failures | 0 |
| Average latency | 30.1s |
| P50 latency | 31s |
| P95 latency | 53s |
| P99 latency | 53s |
| Throughput | 0.29 req/s |

## Observations

- The server remained stable under both 10-user and 50-user load tests.
- Both load tests completed with zero failed requests.
- Latency increased significantly at 50 users because the local server only had 2 parallel slots, so most requests waited in queue.
- Throughput decreased from 0.48 req/s at 10 users to 0.29 req/s at 50 users, showing that this laptop is compute-bound under high concurrency.
- For interactive local usage, the server is usable. For high-concurrency serving, the model/server would need more parallel slots, a smaller model, lower max tokens, or stronger GPU resources.

## Evidence Files

- `benchmarks/02-locust-10_stats.csv`
- `benchmarks/02-locust-10_stats_history.csv`
- `benchmarks/02-locust-10_failures.csv`
- `benchmarks/02-locust-10_exceptions.csv`
- `benchmarks/02-locust-50_stats.csv`
- `benchmarks/02-locust-50_stats_history.csv`
- `benchmarks/02-locust-50_failures.csv`
- `benchmarks/02-locust-50_exceptions.csv`
- `benchmarks/02-server-smoke.md`
- `benchmarks/02-server-metrics.md`
