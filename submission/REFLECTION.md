
# Reflection — Lab 20 (Personal Report)



> This is my individual lab report, completed on my own laptop using my own hardware setup, measurements, and tuning decisions.



---



**Full name:** Thái Thị Yến Nhi  

**Student ID:** 2A202600783  

**Cohort:** A20-K2  

**Submission date:** 2026-06-24



---



## 1. Hardware spec



- **OS:** Windows 11 + Ubuntu WSL2

- **CPU:** Intel Core i9-14900HX

- **Cores:** 24 physical / 32 logical

- **CPU extensions:** AVX2 / AVX-512 capable CPU family

- **RAM:** 32GB DDR5

- **Accelerator:** NVIDIA GeForce RTX 4060 Laptop GPU 8GB

- **Selected llama.cpp backend:** CUDA

- **Recommended model tier:** Qwen2.5-7B-Instruct



**Setup story**



I used Ubuntu WSL2 instead of running everything directly on Windows because CUDA and native llama.cpp builds were more reliable there. I installed CUDA tooling, created a Python virtual environment, built CUDA-enabled llama-cpp-python, downloaded Qwen2.5 GGUF models, then built the native `llama-server` to expose `/metrics`.



---



## 2. Track 01 — Quickstart numbers



| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |

|---|--:|--:|--:|--:|--:|

| Qwen2.5-7B-Instruct Q4_K_M | 5813 | 58 / 76 | 28.6 / 34.5 | 1853 / 2033 / 2055 | 34.9 |

| Qwen2.5-7B-Instruct Q2_K | 2091 | 45 / 61 | 25.4 / 29.0 | 1638 / 1705 / 1723 | 39.3 |



**Observation**



Q2_K is faster and lighter, but Q4_K_M is still fast enough on my RTX 4060 Laptop GPU and should preserve better answer quality. I used Q4_K_M as the primary serving model and kept Q2_K only for comparison.



---



## 3. Track 02 — llama-server load test



| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |

|--:|--:|--:|--:|--:|--:|

| 10 | 0.48 | 18000 | 22000 | 23000 | 0 |

| 50 | 0.29 | 31000 | 53000 | 53000 | 0 |



**KV-cache observation**



The native `llama-server` metrics endpoint was available and returned Prometheus metrics such as `llamacpp:prompt_tokens_total`, `llamacpp:tokens_predicted_total`, `llamacpp:prompt_tokens_seconds`, and `llamacpp:predicted_tokens_seconds`. In this run, I did not capture a direct `llamacpp:kv_cache_usage_ratio` value, so I interpreted the load test through request latency and failures. At concurrency 50, failures stayed at 0, but latency increased sharply because the server used only 2 parallel slots and most requests waited in queue.



---



## 4. Track 03 — Milestone integration



- **N16 Cloud/IaC:** stub: localhost only

- **N17 Data pipeline:** stub: in-memory retrieval

- **N18 Lakehouse:** stub: toy documents

- **N19 Vector + Feature Store:** stub: `TOY_DOCS`



**Slowest part of the pipeline**



- embed: 0 ms

- retrieve: about 0 ms

- llama-server: about 2774 ms average across the three sample queries



**Reflection**



The bottleneck was clearly llama-server generation time, not retrieval. This matched my expectation because retrieval was only an in-memory stub, while the local 7B model still had to run real inference on the GPU.



---



## 5. Bonus — The single change that mattered most



**Change:** Quantization comparison: Q4_K_M vs Q2_K. Q2_K reduced memory use and improved decode speed, while Q4_K_M remained my chosen default because it should preserve better answer quality.



**Before vs after**



~~~text

before: Q4_K_M decode rate = 34.9 tok/s, TPOT P50 = 28.6 ms

after:  Q2_K decode rate = 39.3 tok/s, TPOT P50 = 25.4 ms

speedup: about 1.13x by decode rate

~~~



**Why it worked**



Q2_K uses a smaller quantized representation than Q4_K_M, so the model loads faster and each decoding step has less memory traffic. On a laptop GPU, memory bandwidth and VRAM pressure matter a lot. That is why Q2_K improved load time, TPOT, and decode rate.



However, I still selected Q4_K_M for the main server because the speed gain from Q2_K was modest compared with the expected quality loss. For a local assistant-style workflow, answer quality is more valuable than a small speedup, especially because Q4_K_M already reached about 34.9 tok/s on my machine.



---



## 6. Optional — The most surprising part



The most surprising part was that the Python server could serve OpenAI-compatible chat completions, but the native `llama-server` was needed to expose `/metrics`. Building the native server was harder than running the model itself because WSL memory limits caused the first build attempts to fail.



---



## 7. Self-graded checklist



- [x] `hardware.json` is ready

- [x] `models/active.json` is ready or the model path snapshot is documented

- [x] `benchmarks/01-quickstart-results.md` is ready

- [x] `benchmarks/02-server-results.md` is ready

- [x] `benchmarks/bonus-*.md` is ready

- [ ] At least 6 screenshots are saved in `submission/screenshots/`

- [ ] `make verify` exits with code 0

- [ ] The GitHub repository is public

- [ ] The public repo URL has been submitted to VinUni LMS



---



**Note:** I will keep the repository accessible during the grading period so the instructor can review my submission. 

