# Milestone 1 End-to-End Live Demo

## Goal

This document describes the live demo for Milestone 1.

The demo proves that the platform can connect:

Day19 hybrid retrieval -> Day20 prompt assembly -> Day20 llama-server response.

## Services used

| Service | Port | Purpose |
|---|---:|---|
| Day19 FastAPI search API | 8000 | Hybrid keyword + vector retrieval |
| Day20 llama-server | 8080 | OpenAI-compatible local LLM serving |
| Day20 pipeline.py | local process | Calls Day19 retrieval, builds prompt, calls Day20 model endpoint |

## Expected live flow

1. User asks a question.
2. `03-milestone-integration/pipeline.py` sends the question to Day19 `/search`.
3. Day19 returns top-k hybrid search contexts.
4. Day20 builds a grounded RAG prompt from those contexts.
5. Day20 sends the prompt to llama-server `/v1/chat/completions`.
6. llama-server returns the answer.
7. The pipeline prints context IDs, scores, timings, and final answer.

## Required terminals

Use three WSL terminals.

### Terminal 1 — Start Day19 API

Go to the Day19 repo:

    cd /home/emin98/labs/Day19-Track2-VectorFeatureStore-Lab

Start the Day19 stack/API according to the path used in the Day19 submission.

Recommended if Docker path is used:

    docker compose up -d
    make api

Health check:

    curl http://localhost:8000/healthz

Search smoke test:

    curl "http://localhost:8000/search?q=cloud%20autoscaling&mode=hybrid&top_k=3"

### Terminal 2 — Start Day20 llama-server

Go to the Day20 repo:

    cd /home/emin98/labs/Day20-Track2-ModelServing-Lab

Start the server:

    make serve

Health/model check from another terminal:

    curl http://localhost:8080/v1/models

### Terminal 3 — Run final integration demo

Go to the Day20 repo:

    cd /home/emin98/labs/Day20-Track2-ModelServing-Lab

Run:

    python 03-milestone-integration/pipeline.py

## Expected output

The script should print something like:

    Day20 real integration pipeline
    Day19 retrieval: http://localhost:8000/search mode= hybrid top_k= 3
    Day20 llama-server: http://localhost:8080/v1 model= local

For each query, it should print:

    contexts:
      - <doc_id> | score=<score> | <title>
    timings : {'retrieve': ..., 'llm': ..., 'total': ...}
    answer  : <generated answer>

## Demo queries

The current pipeline uses these built-in queries:

- Tự động mở rộng hạ tầng theo lưu lượng người dùng là gì?
- Schema evolution không phá vỡ downstream nghĩa là gì?
- Zero trust và MFA giúp bảo mật hệ thống như thế nào?

## Evidence files

The successful run is documented by:

- `benchmarks/03-day19-healthz.json`
- `benchmarks/03-day19-search-sample.json`
- `benchmarks/03-real-rag-pipeline-output.txt`
- `benchmarks/03-real-integration-summary.md`
- `submission/screenshots/07-real-rag-pipeline.png`

## What this proves

This demo proves the final serving path of the AI infrastructure platform:

- Day19 retrieval is real, not a toy in-memory stub.
- Day20 receives real retrieved contexts.
- Day20 calls a local OpenAI-compatible model endpoint.
- The system returns a grounded answer with context IDs and latency timings.
