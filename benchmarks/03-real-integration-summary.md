# Day20 Real Integration Summary

This milestone replaces the original toy retrieval stub with a real integration between Day19 and Day20.

## Real services used

- Day19 search API: `http://localhost:8000/search`
- Day19 retrieval mode: `hybrid`
- Day19 top_k: `3`
- Day20 llama-server: `http://localhost:8080/v1/chat/completions`
- Model endpoint verified through `/v1/models`

## What changed

- Removed the in-memory toy retrieval path from `03-milestone-integration/pipeline.py`.
- Added real HTTP retrieval from Day19 `/search`.
- Normalized Day19 hits into Day20 `Doc` contexts with `doc_id`, `title`, `text`, and `score`.
- Built the LLM prompt from real Day19 retrieved contexts.
- Kept the existing OpenAI-compatible llama-server call.

## Evidence

- `benchmarks/03-day19-healthz.json`
- `benchmarks/03-day19-search-sample.json`
- `benchmarks/03-real-rag-pipeline-output.txt`

## Result

The real RAG pipeline successfully retrieved Day19 contexts and generated answers through Day20 llama-server for three test queries.
