#!/usr/bin/env python3
"""Real RAG pipeline: Day19 hybrid search API + Day20 llama-server.

This pipeline uses real retrieval from the Day19 `/search` endpoint.

Required services:
  1. Day19 FastAPI search API on http://localhost:8000
  2. Day20 llama-server OpenAI-compatible API on http://localhost:8080/v1

Useful env vars:
  DAY19_SEARCH_URL=http://localhost:8000/search
  DAY19_SEARCH_MODE=hybrid
  DAY19_TOP_K=3
  DAY19_RRF_K=60
  LLAMA_SERVER_BASE=http://localhost:8080/v1
  LLAMA_MODEL=local
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Iterable, Any

import httpx


DAY19_SEARCH_URL = os.getenv("DAY19_SEARCH_URL", "http://localhost:8000/search")
DAY19_SEARCH_MODE = os.getenv("DAY19_SEARCH_MODE", "hybrid")
DAY19_TOP_K = int(os.getenv("DAY19_TOP_K", "3"))
DAY19_RRF_K = int(os.getenv("DAY19_RRF_K", "60"))

LLAMA_SERVER_BASE = os.getenv("LLAMA_SERVER_BASE", "http://localhost:8080/v1").rstrip("/")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "local")

SYSTEM_PROMPT = (
    "You are a serving-engineering tutor. Answer using only the retrieved Day19 documents. "
    "If the documents do not contain the answer, say so. "
    "Prefer concise Vietnamese answers when the context is Vietnamese."
)


@dataclass
class Doc:
    id: str
    title: str
    text: str
    score: float


def _coerce_hit(hit: dict[str, Any]) -> Doc:
    """Normalize Day19 search hit shape into the Day20 pipeline Doc shape."""
    return Doc(
        id=str(hit.get("doc_id") or hit.get("id") or hit.get("document_id") or "unknown"),
        title=str(hit.get("title") or ""),
        text=str(hit.get("text") or hit.get("content") or ""),
        score=float(hit.get("score") or 0.0),
    )


def retrieve(query: str, k: int = DAY19_TOP_K) -> list[Doc]:
    """Retrieve real contexts from Day19 hybrid search API."""
    params = {
        "q": query,
        "mode": DAY19_SEARCH_MODE,
        "top_k": k,
        "rrf_k": DAY19_RRF_K,
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(DAY19_SEARCH_URL, params=params)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Day19 retrieval failed. Make sure Day19 API is running:\n"
            "  cd ~/labs/Day19-Track2-VectorFeatureStore-Lab\n"
            "  source .venv/bin/activate\n"
            "  docker compose up -d\n"
            "  make api\n"
            f"Original error: {exc}"
        ) from exc

    payload = response.json()
    raw_hits = payload.get("hits")
    if raw_hits is None:
        raw_hits = payload.get("results", [])

    docs = [_coerce_hit(hit) for hit in raw_hits[:k]]
    if not docs:
        raise RuntimeError(f"Day19 returned no hits for query={query!r}. Payload={payload}")

    return docs


def build_prompt(query: str, contexts: Iterable[Doc]) -> list[dict[str, str]]:
    ctx_lines: list[str] = []
    for i, c in enumerate(contexts, start=1):
        title = f" — {c.title}" if c.title else ""
        ctx_lines.append(
            f"[{i}] doc_id={c.id}{title}\n"
            f"score={c.score:.6f}\n"
            f"{c.text}"
        )

    ctx_block = "\n\n".join(ctx_lines)
    user = (
        f"Retrieved Day19 context:\n{ctx_block}\n\n"
        f"Question: {query}\n\n"
        "Answer using the retrieved context only. Mention the most relevant doc_id when useful."
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def call_llm(messages: list[dict[str, str]]) -> tuple[str, float]:
    t0 = time.perf_counter()

    try:
        response = httpx.post(
            f"{LLAMA_SERVER_BASE}/chat/completions",
            json={
                "model": LLAMA_MODEL,
                "messages": messages,
                "max_tokens": 220,
                "temperature": 0.2,
            },
            timeout=180.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "llama-server call failed. Make sure Day20 llama-server is running on port 8080.\n"
            f"LLAMA_SERVER_BASE={LLAMA_SERVER_BASE}\n"
            f"Original error: {exc}"
        ) from exc

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    payload = response.json()
    text = payload["choices"][0]["message"]["content"]
    return text, elapsed_ms


def answer(query: str, k: int = DAY19_TOP_K) -> dict[str, Any]:
    t_total = time.perf_counter()

    t = time.perf_counter()
    docs = retrieve(query, k=k)
    t_retrieve_ms = (time.perf_counter() - t) * 1000.0

    messages = build_prompt(query, docs)

    text, t_llm_ms = call_llm(messages)

    return {
        "query": query,
        "answer": text,
        "contexts": [
            {
                "id": d.id,
                "title": d.title,
                "score": d.score,
                "text_preview": d.text[:180],
            }
            for d in docs
        ],
        "timings_ms": {
            "retrieve": round(t_retrieve_ms, 1),
            "llm": round(t_llm_ms, 1),
            "total": round((time.perf_counter() - t_total) * 1000.0, 1),
        },
        "config": {
            "day19_search_url": DAY19_SEARCH_URL,
            "day19_search_mode": DAY19_SEARCH_MODE,
            "top_k": k,
            "llama_server_base": LLAMA_SERVER_BASE,
            "llama_model": LLAMA_MODEL,
        },
    }


def main() -> None:
    queries = [
        "Tự động mở rộng hạ tầng theo lưu lượng người dùng là gì?",
        "Schema evolution không phá vỡ downstream nghĩa là gì?",
        "Zero trust và MFA giúp bảo mật hệ thống như thế nào?",
    ]

    print("Day20 real integration pipeline")
    print("Day19 retrieval:", DAY19_SEARCH_URL, "mode=", DAY19_SEARCH_MODE, "top_k=", DAY19_TOP_K)
    print("Day20 llama-server:", LLAMA_SERVER_BASE, "model=", LLAMA_MODEL)

    for q in queries:
        print(f"\n=== {q} ===")
        result = answer(q, k=DAY19_TOP_K)
        print("  contexts:")
        for c in result["contexts"]:
            print(f"    - {c['id']} | score={c['score']:.6f} | {c['title'][:80]}")
        print(f"  timings : {result['timings_ms']}")
        print(f"  answer  : {result['answer'].strip()[:600]}")


if __name__ == "__main__":
    main()
