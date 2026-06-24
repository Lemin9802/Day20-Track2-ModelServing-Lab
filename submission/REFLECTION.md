# Reflection — Lab 20: Model Serving & Real RAG Integration

> This is my individual lab report, completed on my own laptop using my own hardware setup, measurements, tuning decisions, and final Day19 + Day20 real integration.

---

**Full name:** Thái Thị Yến Nhi  
**Student ID:** 2A202600783  
**Cohort:** A20-K2  
**Submission date:** 2026-06-24

---

## 1. Hardware spec

| Item | Value |
|---|---|
| OS | Windows 11 + Ubuntu WSL2 |
| CPU | Intel Core i9-14900HX |
| Cores | 24 cores / 32 logical threads |
| RAM | 32GB DDR5 |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU 8GB |
| Selected llama.cpp backend | CUDA |
| Main model tier | Qwen2.5-7B-Instruct GGUF |
| Primary serving model | Q4_K_M |
| Comparison model | Q2_K |

### Setup story

I used Ubuntu WSL2 instead of running everything directly on Windows because CUDA and native llama.cpp builds were more reliable there. I installed CUDA tooling, created a Python virtual environment, built CUDA-enabled `llama-cpp-python`, downloaded Qwen2.5 GGUF models, and then built the native `llama-server` so I could expose both OpenAI-compatible chat completions and Prometheus-style `/metrics`.

---

## 2. Track 01 — Quickstart numbers

| Model | Load (ms) | TTFT P50 (ms) | TTFT P95 (ms) | TPOT P50 (ms) | TPOT P95 (ms) | E2E P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Decode rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct Q4_K_M | 5813 | 58 | 76 | 28.6 | 34.5 | 1853 | 2033 | 2055 | 34.9 tok/s |
| Qwen2.5-7B-Instruct Q2_K | 2091 | 45 | 61 | 25.4 | 29.0 | 1638 | 1705 | 1723 | 39.3 tok/s |

### Observation

Q2_K loaded faster and decoded faster than Q4_K_M. However, I selected Q4_K_M as the primary serving model because it still performed well on my RTX 4060 Laptop GPU while preserving better expected answer quality. Q2_K was useful as a comparison point, but Q4_K_M was the better default for a local assistant-style workflow.

---

## 3. Track 02 — llama-server load test

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|---:|---:|---:|---:|---:|---:|
| 10 users | 0.48 | 18000 | 22000 | 23000 | 0 |
| 50 users | 0.29 | 31000 | 53000 | 53000 | 0 |

### KV-cache and queueing observation

The native `llama-server` metrics endpoint was available and returned Prometheus metrics such as `llamacpp:prompt_tokens_total`, `llamacpp:tokens_predicted_total`, `llamacpp:prompt_tokens_seconds`, and `llamacpp:predicted_tokens_seconds`.

In this run, I did not capture a direct `llamacpp:kv_cache_usage_ratio` value, so I interpreted server behavior through latency and failure rate. At 50 concurrent users, the failure count stayed at 0, but latency increased sharply. This suggests the bottleneck was not request failure, but queueing and limited parallel serving capacity. The server could handle the load, but users waited much longer when concurrency increased.

---

## 4. Track 03 — Real Day19 + Day20 RAG integration

The original milestone pipeline started with toy in-memory retrieval. I replaced that path with a real integration to my Day19 hybrid search API.

### Final integration flow

| Component | Final status |
|---|---|
| Day19 vector search API | Real `/search` endpoint on `localhost:8000` |
| Retrieval mode | `hybrid` |
| Retrieved context fields | `doc_id`, `title`, `text`, `score` |
| Day20 pipeline | Builds prompt from real Day19 contexts |
| LLM serving | Native `llama-server` OpenAI-compatible endpoint |
| LLM endpoint | `http://localhost:8080/v1/chat/completions` |
| Evidence | `benchmarks/03-real-rag-pipeline-output.txt` and `submission/screenshots/07-real-rag-pipeline.png` |

### Example real outputs

| Query | Example retrieved docs | Result |
|---|---|---|
| Tự động mở rộng hạ tầng theo lưu lượng người dùng là gì? | `cloud_036`, `cloud_000`, `cloud_033` | Answer generated from real cloud contexts |
| Schema evolution không phá vỡ downstream nghĩa là gì? | `data_eng_044`, `data_eng_085`, `data_eng_026` | Answer generated from real data engineering contexts |
| Zero trust và MFA giúp bảo mật hệ thống như thế nào? | `security_054`, `security_052`, `security_096` | Answer generated from real security contexts |

### Slowest part of the real pipeline

| Query area | Retrieve time | LLM time | Total time |
|---|---:|---:|---:|
| Cloud autoscaling | 137.3 ms | 5785.9 ms | 5923.2 ms |
| Schema evolution | 80.7 ms | 3196.1 ms | 3276.8 ms |
| Security / zero trust | 59.3 ms | 2835.6 ms | 2895.0 ms |

The bottleneck was clearly llama-server generation time, not Day19 retrieval. Retrieval stayed under 150 ms in the real integration run, while generation took several seconds. This matches the expected behavior of a local 7B model: retrieval is lightweight, but autoregressive token generation dominates end-to-end latency.

---

## 5. Bonus — The single change that mattered most

**Change:** Quantization comparison between Q4_K_M and Q2_K.

| Model | Decode rate | TPOT P50 | Load time |
|---|---:|---:|---:|
| Q4_K_M | 34.9 tok/s | 28.6 ms | 5813 ms |
| Q2_K | 39.3 tok/s | 25.4 ms | 2091 ms |

**Speedup:** Q2_K achieved about **1.13x** higher decode rate than Q4_K_M.

### Why it worked

Q2_K uses a smaller quantized representation than Q4_K_M, so it reduces memory pressure and improves decode speed. On a laptop GPU, memory bandwidth and VRAM pressure matter a lot. That is why Q2_K improved load time, TPOT, and decode rate.

However, I still selected Q4_K_M for the main server because the speed gain from Q2_K was modest compared with the expected answer-quality loss. For a local assistant workflow, quality is more valuable than a small speedup, especially because Q4_K_M already reached about 34.9 tok/s on my machine.

---

## 6. Most surprising part

The most surprising part was that running an OpenAI-compatible chat server was easier than getting full observability and native metrics. The Python path was convenient, but the native `llama-server` was needed to expose `/metrics`. Building the native server in WSL required more care than the model serving itself because local memory limits made early build attempts unstable.

The second surprise was the real RAG integration result: after connecting Day20 to Day19, retrieval latency was much smaller than generation latency. This helped me understand why production model serving work often focuses heavily on batching, KV cache efficiency, quantization, and concurrency control.

---

## 7. Self-graded checklist

- [x] `hardware.json` is ready.
- [x] Model path is documented through `/v1/models`, benchmark files, and screenshots.
- [x] `benchmarks/01-quickstart-results.md` is ready.
- [x] `benchmarks/02-server-results.md` is ready.
- [x] `benchmarks/bonus-quantization-summary.md` is ready.
- [x] At least 6 screenshots are saved in `submission/screenshots/`.
- [x] Screenshot `07-real-rag-pipeline.png` documents the real Day19 + Day20 integration.
- [x] `SUBMISSION.md` is ready for grading.
- [x] `README.md` links to `SUBMISSION.md`.
- [x] The GitHub repository has been committed and pushed.
- [x] The public repo URL is ready to submit to VinUni LMS.

---

## 8. Final repository

Repository:

`https://github.com/Lemin9802/Day20_2A202600783_Thai-Thi-Yen-Nhi`

I will keep the repository accessible during the grading period so the instructor can review my submission.
