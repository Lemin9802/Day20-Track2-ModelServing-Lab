# Milestone 1 — AI Infrastructure Platform Demo

## Goal

This milestone packages the Day16 to Day20 work into one coherent AI infrastructure platform demo.

The final platform connects:

- N16 / Day16: Cloud infrastructure and IaC
- N17 / Day17: Data pipeline and processing
- N18 / Day18: Delta Lakehouse and Medallion architecture
- N19 / Day19: Vector store, hybrid semantic search, and feature store
- N20 / Day20: Optimized model serving endpoint, benchmark report, and live end-to-end demo

## End-to-end demo flow

User query
-> Day19 hybrid search API
-> retrieved context from vector store
-> Day20 prompt assembly
-> Day20 llama-server OpenAI-compatible endpoint
-> final answer
-> latency / benchmark evidence

## Slide requirement mapping

| Milestone requirement | Implementation evidence |
|---|---|
| 1. Cloud setup: IaC + cluster/cloud infra | Day16 Terraform-managed GCP infrastructure with VPC, subnet, NAT, firewall, VM, load balancer, benchmark, billing evidence, and cleanup |
| 2. Data pipeline: ingestion + processing | Day17 validation/quarantine, Silver deduplication, Gold aggregation, RAG ingestion, point-in-time feature correctness, and verification logs |
| 3. Lakehouse: Delta Lake + Medallion | Day18 Delta Lakehouse with Bronze/Silver/Gold, lightweight path, Spark/Docker path, Delta optimization, time travel, and bonus architecture |
| 4. Vector store: semantic search API | Day19 Qdrant-backed vector search and hybrid search API |
| 5. Feature store: online/offline | Day19 Feast feature store with Redis online store and point-in-time historical joins |
| 6. Model serving: optimized endpoint | Day20 llama.cpp / llama-server OpenAI-compatible /v1/chat/completions endpoint |
| 7. Benchmark report: latency + cost | Day19 search/feature latency plus Day20 quickstart, Locust 10-user and 50-user load tests |
| 8. Live demo: end-to-end flow | Day19 /search retrieval integrated with Day20 03-milestone-integration/pipeline.py and llama-server |

## Component summary

### N16 / Day16 — Cloud infrastructure

Repository:

- https://github.com/Lemin9802/2A202600783_Thai-Thi-Yen-Nhi_Day16_Lab

Evidence summary:

- Google Cloud Platform deployment
- Terraform Infrastructure as Code
- Custom VPC, subnet, NAT, firewall rules, service account
- VM instance and HTTP load balancer
- CPU fallback because GCP GPU quota was unavailable
- ML benchmark and billing/cleanup evidence

Note:

The original cloud GPU target could not be provisioned because the GCP project had zero GPU quota. The milestone therefore uses Day16 as cloud/IaC evidence and Day20 local GPU serving as the model-serving evidence.

### N17 / Day17 — Data pipeline

Repository:

- https://github.com/Lemin9802/Day17_2A202600783_Thai-Thi-Yen-Nhi

Evidence summary:

- Core Medallion-style data pipeline
- Validation and quarantine flow
- Silver deduplication
- Gold aggregation
- Streaming idempotency
- RAG ingestion
- Agent trace flywheel
- Point-in-time feature correctness
- Knowledge Graph demo
- verify.py: 16/16 checks passed
- Pytest: 18 passed

### N18 / Day18 — Lakehouse

Repository:

- https://github.com/Lemin9802/Day18-Track2-Lakehouse-Lab

Evidence summary:

- Lightweight path with deltalake, DuckDB, and Polars
- Spark/Docker path with PySpark, Delta Lake, and MinIO
- Bronze -> Silver -> Gold medallion pipeline
- Delta schema evolution, OPTIMIZE/Z-order, time travel, RESTORE, and MERGE
- Bonus architecture challenge: LLM Observability Lakehouse at 1B Requests/Day
- Optional PII redaction/tokenization PoC
- Individual reflection, screenshots, and verification logs

Spark NB4 medallion result:

- Bronze rows: 200000
- Silver rows: 190086
- Dedup dropped: 9914
- Gold rows: 21
- Distinct dates: 7
- Distinct models: 3

Note:

Spark make spark-data with the default 1M rows hit local Java heap limits, so a 200K-row Spark Bronze dataset was used. The medallion checks still passed.

### N19 / Day19 — Vector store and feature store

Repository:

- https://github.com/Lemin9802/Day19_2A202600783_Thai-Thi-Yen-Nhi

Evidence summary:

- Qdrant vector store
- Hybrid search API with keyword, semantic, and hybrid modes
- 1,000 documents indexed
- Final benchmark Precision@10:
  - Keyword: 77.8%
  - Semantic: 73.2%
  - Hybrid: 78.6%
- Hybrid P99 latency: 18.7 ms
- Feast feature store with 3 feature views
- Redis online store
- Feast online lookup P99: 5.41 ms

### N20 / Day20 — Model serving and final integration

Current repository:

- https://github.com/Lemin9802/Day20_2A202600783_Thai-Thi-Yen-Nhi

Evidence summary:

- llama.cpp / llama-server serving
- OpenAI-compatible /v1/chat/completions endpoint
- Qwen2.5-7B-Instruct Q4_K_M model
- CUDA backend on NVIDIA RTX 4060 Laptop GPU
- Quickstart benchmark with TTFT, TPOT, E2E P50/P95/P99
- Locust load test with 10 and 50 concurrent users
- Real Day19 + Day20 RAG integration

## Live demo script

The live demo starts two services:

1. Day19 FastAPI search API on port 8000
2. Day20 llama-server on port 8080

Then run:

python 03-milestone-integration/pipeline.py

Expected result:

- The pipeline sends a query to Day19 /search
- Day19 returns hybrid search contexts
- Day20 assembles the prompt
- llama-server generates the final answer
- The script prints contexts, timings, and answer text

## Submission files for Milestone 1

- MILESTONE1.md
- architecture/milestone1-architecture.md
- integration/end_to_end_demo.md
- integration/runbook.md
- benchmarks/milestone1-latency-cost.md
- SUBMISSION.md
- benchmarks/03-real-integration-summary.md
- benchmarks/03-real-rag-pipeline-output.txt
- submission/screenshots/07-real-rag-pipeline.png
