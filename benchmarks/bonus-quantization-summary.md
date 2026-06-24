# Bonus — Quantization Comparison Summary

## Change Tested

I compared two quantization levels for the same Qwen2.5-7B-Instruct model:

- Q4_K_M
- Q2_K

The main change was using the smaller Q2_K quantization to reduce memory traffic and improve decoding speed.

## Results

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|--:|--:|--:|--:|--:|
| Qwen2.5-7B-Instruct Q4_K_M | 5813 | 58 / 76 | 28.6 / 34.5 | 1853 / 2033 / 2055 | 34.9 |
| Qwen2.5-7B-Instruct Q2_K | 2091 | 45 / 61 | 25.4 / 29.0 | 1638 / 1705 / 1723 | 39.3 |

## Before vs After

~~~text
before: Q4_K_M decode rate = 34.9 tok/s, TPOT P50 = 28.6 ms
after:  Q2_K decode rate = 39.3 tok/s, TPOT P50 = 25.4 ms
speedup: about 1.13x by decode rate
~~~

## Observation

Q2_K loaded faster and decoded faster than Q4_K_M because it uses a smaller quantized representation. This reduces memory traffic and VRAM pressure, which matters on a laptop GPU.

However, the speedup was modest. I kept Q4_K_M as the primary serving model because it should preserve better answer quality while still reaching about 34.9 tok/s on my RTX 4060 Laptop GPU.
