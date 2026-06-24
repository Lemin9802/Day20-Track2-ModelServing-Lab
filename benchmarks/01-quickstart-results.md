# 01 — Quickstart Results

Settings: `n_threads=24`, `n_ctx=2048`, `n_batch=512`, `n_gpu_layers=99`.

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|---:|---:|---:|---:|---:|
| qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf | 5813 | 58 / 76 | 28.6 / 34.5 | 1853 / 2033 / 2055 | 34.9 |
| qwen2.5-7b-instruct-q2_k.gguf | 2091 | 45 / 61 | 25.4 / 29.0 | 1638 / 1705 / 1723 | 39.3 |

## Observations

- CUDA acceleration worked correctly on the RTX 4060 Laptop GPU. The Q4_K_M model loaded successfully and all layers were offloaded to GPU during the smoke test.
- Q4_K_M is the better default model for this machine because it still reaches about 34.9 tok/s while preserving better output quality than Q2_K.
- Q2_K is faster and lighter: TPOT P50 improved from 28.6 ms to 25.4 ms, and decode rate improved from 34.9 tok/s to 39.3 tok/s.
- Q4_K_M takes longer to load than Q2_K, about 5.8s versus 2.1s, but this cost is paid once when the model/server starts.
- TTFT is low for both quantizations on short prompts, with Q4_K_M P95 around 76 ms and Q2_K P95 around 61 ms.
- For the rest of the lab, I will use Q4_K_M as the primary model and Q2_K only as a comparison model.
