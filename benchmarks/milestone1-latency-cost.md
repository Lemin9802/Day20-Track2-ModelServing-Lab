# Milestone 1 Benchmark Report — Latency and Cost

## Purpose

This file summarizes the benchmark evidence across the Milestone 1 platform:

- Day19 retrieval and feature-serving latency
- Day20 model serving latency
- Day20 load-test behavior under 10 and 50 concurrent users
- Cost and deployment notes

## Day19 retrieval and feature layer

Source evidence:

- Day19 repository: https://github.com/Lemin9802/Day19_2A202600783_Thai-Thi-Yen-Nhi
- Day19 submission summary: `SUBMISSION.md`

Results:

| Metric | Value |
|---|---:|
| Corpus indexed | 1,000 documents |
| Keyword Precision@10 | 77.8% |
| Semantic Precision@10 | 73.2% |
| Hybrid Precision@10 | 78.6% |
| Hybrid search P99 latency | 18.7 ms |
| Feast feature views | 3 |
| Feast online lookup P99 | 5.41 ms |

Interpretation:

Hybrid retrieval is used in the final demo because it performed better than keyword-only and semantic-only retrieval on the Day19 benchmark.

## Day20 quickstart model-serving benchmark

Source evidence:

- `benchmarks/01-quickstart-results.md`

Configuration:

| Item | Value |
|---|---|
| Runtime | llama.cpp / llama-cpp-python |
| Primary model | Qwen2.5-7B-Instruct Q4_K_M |
| Backend | CUDA |
| GPU | NVIDIA RTX 4060 Laptop GPU |
| Threads | 24 |
| Context size | 2048 |
| GPU layers | 99 |

Primary model result:

| Metric | Value |
|---|---:|
| Load time | 5813 ms |
| TTFT P50 | 58 ms |
| TTFT P95 | 76 ms |
| TPOT P50 | 28.6 ms |
| TPOT P95 | 34.5 ms |
| E2E P50 | 1853 ms |
| E2E P95 | 2033 ms |
| E2E P99 | 2055 ms |
| Decode rate | 34.9 tok/s |

Comparison model:

| Model | E2E P50 | E2E P95 | E2E P99 | Decode rate |
|---|---:|---:|---:|---:|
| Q4_K_M | 1853 ms | 2033 ms | 2055 ms | 34.9 tok/s |
| Q2_K | 1638 ms | 1705 ms | 1723 ms | 39.3 tok/s |

Interpretation:

Q2_K is faster and lighter, but Q4_K_M is used as the primary model because it preserves better quality while still achieving usable local inference speed.

## Day20 load test

Source evidence:

- `benchmarks/02-load-test-summary.md`

Server configuration:

| Item | Value |
|---|---|
| Server | native llama-server |
| Endpoint | http://127.0.0.1:8080/v1/chat/completions |
| Model | Qwen2.5-7B-Instruct Q4_K_M |
| Backend | CUDA |
| GPU | NVIDIA RTX 4060 Laptop GPU |
| Context size | 2048 |
| GPU layers | 99 |
| Threads | 24 |
| Parallel slots | 2 |
| Continuous batching | enabled |
| Metrics endpoint | enabled |

10 concurrent users:

| Metric | Value |
|---|---:|
| Total requests | 28 |
| Failures | 0 |
| Average latency | 15.5 s |
| P50 latency | 18 s |
| P95 latency | 22 s |
| P99 latency | 23 s |
| Throughput | 0.48 req/s |

50 concurrent users:

| Metric | Value |
|---|---:|
| Total requests | 16 |
| Failures | 0 |
| Average latency | 30.1 s |
| P50 latency | 31 s |
| P95 latency | 53 s |
| P99 latency | 53 s |
| Throughput | 0.29 req/s |

Interpretation:

The server stayed stable with zero failed requests. Latency increased at 50 users because the laptop server used only 2 parallel slots, so many requests waited in queue. For higher concurrency, the platform would need more parallel slots, a smaller model, lower max tokens, or stronger GPU resources.

## Cost note

Day16 cloud infrastructure was provisioned on GCP through Terraform, but GPU serving on cloud was not used because the GCP project had zero GPU quota.

For Milestone 1:

- Cloud/IaC evidence comes from Day16.
- Final inference serving is performed locally on the laptop RTX 4060 GPU.
- This avoids cloud GPU cost for the demo.
- Production deployment would require right-sizing GPU, model quantization, autoscaling, and queue-depth based monitoring.

## Goodput and SLO note

The local demo is optimized for correctness and reproducibility rather than high-concurrency production goodput.

A reasonable local-demo SLO is:

| Metric | Target |
|---|---:|
| Retrieval P99 | < 100 ms |
| Quickstart E2E P95 | < 3 s |
| 10-user load-test failures | 0 |
| 50-user load-test failures | 0 |

The current evidence meets the retrieval target, quickstart target, and zero-failure load-test target. It does not target production-scale concurrency on a single laptop GPU.
