# Day 20 Submission Summary — Model Serving & Real RAG Integration

## Quick Status

This submission completes the Day20 model serving lab evidence and adds a real integration milestone using Day19 hybrid search.

## Completed Scope

- Hardware probe completed.
- llama.cpp quickstart benchmark completed.
- llama-server started and verified.
- Locust/load-test evidence collected.
- Bonus quantization / sweep evidence collected.
- Real RAG integration completed by replacing the toy retrieval stub with Day19 `/search`.
- README/SUBMISSION evidence prepared for grading.

## Real Integration Result

The original `03-milestone-integration/pipeline.py` toy retrieval path was replaced with a real HTTP retrieval call to the Day19 search API.

Real flow:

    Day19 /search hybrid retrieval
        -> Day20 pipeline.py prompt assembly
        -> Day20 llama-server /v1/chat/completions
        -> final answer with real retrieved contexts

Services used:

- Day19 API: `http://localhost:8000/search`
- Day19 mode: `hybrid`
- Day19 `top_k`: `3`
- Day20 llama-server: `http://localhost:8080/v1`
- Endpoint verified: `/v1/models`

## Evidence Files

### Screenshots

- [01 Hardware Probe](submission/screenshots/01-hardware-probe.png)
- [02 Quickstart Benchmark](submission/screenshots/02-quickstart-bench.png)
- [03 Server Running](submission/screenshots/03-server-running.png)
- [04 Locust 10 Users](submission/screenshots/04-locust-10.png)
- [05 Locust 50 Users](submission/screenshots/05-locust-50.png)
- [06 Bonus Sweep](submission/screenshots/06-bonus-sweep.png)
- [07 Real RAG Pipeline](submission/screenshots/07-real-rag-pipeline.png)

### Benchmark / Output Logs

- [Quickstart Results JSON](benchmarks/01-quickstart-results.json)
- [Quickstart Results Markdown](benchmarks/01-quickstart-results.md)
- [Server Smoke Result](benchmarks/02-server-smoke.md)
- [Server Results](benchmarks/02-server-results.md)
- [Server Metrics](benchmarks/02-server-metrics.md)
- [Load Test Summary](benchmarks/02-load-test-summary.md)
- [Original Pipeline Output](benchmarks/03-pipeline-output.txt)
- [Real RAG Pipeline Output](benchmarks/03-real-rag-pipeline-output.txt)
- [Real Integration Summary](benchmarks/03-real-integration-summary.md)
- [Day19 Health Check](benchmarks/03-day19-healthz.json)
- [Day19 Search Sample](benchmarks/03-day19-search-sample.json)
- [Bonus Quantization Summary](benchmarks/bonus-quantization-summary.md)

## Key Real Integration Output

The real pipeline retrieved Day19 contexts and generated answers for three queries:

- Cloud autoscaling / hạ tầng tự động mở rộng
- Schema evolution without breaking downstream
- Zero trust and MFA security

Example retrieved context IDs:

- `cloud_036`
- `cloud_000`
- `cloud_033`
- `data_eng_044`
- `security_054`

## Important Note

This real integration does not remove the previous Day20 evidence. Screenshots `01` to `06` remain as the original model-serving evidence. Screenshot `07` and the `03-real-*` benchmark files document the new real Day19 + Day20 integration.
