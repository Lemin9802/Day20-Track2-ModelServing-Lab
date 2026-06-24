# 03 — Milestone Integration Notes

## What Ran

I ran `03-milestone-integration/pipeline.py` against the local native `llama-server` running at `http://127.0.0.1:8080`.

The pipeline executed three sample queries end-to-end:

1. `Why is goodput more useful than throughput?`
2. `What problem does PagedAttention actually solve?`
3. `When should I think about disaggregated serving?`

## Integration Path

The current integration path is:

1. User query
2. In-memory retrieval over toy/stub documents
3. Prompt construction with retrieved context
4. Local OpenAI-compatible request to `/v1/chat/completions`
5. Answer returned from local Qwen2.5-7B-Instruct Q4_K_M model
6. Printed context provenance and timing information

## Real vs Stubbed Components

| Component | Status | Notes |
|---|---|---|
| Local LLM server | Real | Native `llama-server` with CUDA, metrics, continuous batching |
| Model | Real | Qwen2.5-7B-Instruct Q4_K_M GGUF |
| Chat completion API | Real | `/v1/chat/completions` |
| Retrieval | Stub | Uses toy in-memory records from the Day20 repo |
| Vector index / N19 | Stub | No external Day19 vector store wired yet |
| Feature store / Feast | Stub | Not connected in this local pre-class run |
| Lakehouse / N18 | Stub | Not connected in this local pre-class run |

## Evidence

Pipeline output was saved to:

- `benchmarks/03-pipeline-output.txt`

## Observations

- The local server successfully handled integration-style requests from a Python pipeline.
- The pipeline printed retrieved context IDs, LLM latency, total latency, and final answers.
- The retrieved contexts were toy/stub documents, so answer quality depends heavily on the small provided context.
- This is sufficient for a local pre-class run. When the Day16-Day19 artifacts are needed, the stub retrieval can be replaced with the real vector/lakehouse/feature-store pipeline.
