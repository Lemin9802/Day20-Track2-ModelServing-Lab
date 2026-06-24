# Milestone 1 Architecture — AI Infrastructure Platform

## Platform view

```mermaid
flowchart LR
    A["N16 / Day16<br/>Cloud Infrastructure<br/>Terraform + GCP VM/LB"] --> B["N17 / Day17<br/>Data Pipeline<br/>Validation + Silver/Gold + RAG ingestion"]
    B --> C["N18 / Day18<br/>Lakehouse<br/>Delta Bronze/Silver/Gold"]
    C --> D["N19 / Day19<br/>Retrieval + Features<br/>Qdrant Hybrid Search + Feast"]
    D --> E["N20 / Day20<br/>Model Serving<br/>llama-server OpenAI-compatible API"]
    E --> F["Live Demo<br/>User query -> retrieved context -> answer"]
    E --> G["Benchmarks<br/>P50/P95/P99 + Locust 10/50 users"]
```

## Runtime demo path

```mermaid
sequenceDiagram
    participant User
    participant Pipeline as Day20 pipeline.py
    participant Search as Day19 /search API
    participant LLM as Day20 llama-server

    User->>Pipeline: Submit demo query
    Pipeline->>Search: GET /search?q=...&mode=hybrid&top_k=3
    Search-->>Pipeline: Return retrieved contexts
    Pipeline->>Pipeline: Build prompt from Day19 contexts
    Pipeline->>LLM: POST /v1/chat/completions
    LLM-->>Pipeline: Generated answer
    Pipeline-->>User: Context IDs, timings, final answer
```

## Production architecture mapping

```mermaid
flowchart TB
    subgraph Cloud["N16 Cloud / IaC"]
        IAC["Terraform"]
        GCP["GCP VM / VPC / NAT / Firewall / Load Balancer"]
        IAC --> GCP
    end

    subgraph Data["N17 Data Pipeline"]
        RAW["Raw data"]
        VALIDATE["Validation + Quarantine"]
        SILVER17["Silver dedup"]
        GOLD17["Gold aggregation"]
        RAW --> VALIDATE --> SILVER17 --> GOLD17
    end

    subgraph Lakehouse["N18 Lakehouse"]
        BRONZE["Delta Bronze"]
        SILVER18["Delta Silver"]
        GOLD18["Delta Gold"]
        OPT["Optimize / Z-order / Time Travel"]
        BRONZE --> SILVER18 --> GOLD18
        GOLD18 --> OPT
    end

    subgraph Retrieval["N19 Retrieval + Feature Store"]
        QDRANT["Qdrant Vector Store"]
        SEARCH["FastAPI /search hybrid"]
        FEAST["Feast Feature Store"]
        REDIS["Redis Online Store"]
        QDRANT --> SEARCH
        FEAST --> REDIS
    end

    subgraph Serving["N20 Model Serving"]
        PIPE["03-milestone-integration/pipeline.py"]
        LLAMA["llama-server /v1/chat/completions"]
        METRICS["Benchmarks + Locust + Prometheus metrics"]
        PIPE --> LLAMA
        LLAMA --> METRICS
    end

    Cloud --> Data
    Data --> Lakehouse
    Lakehouse --> Retrieval
    Retrieval --> Serving
```

## Design rationale

This architecture keeps each daily lab as a platform component instead of treating the labs as isolated assignments.

- Day16 proves that infrastructure can be provisioned with Infrastructure as Code.
- Day17 proves that raw data can be validated, processed, deduplicated, and promoted into downstream datasets.
- Day18 proves that the platform has a Lakehouse layer with Delta tables, Medallion organization, optimization, and rollback concepts.
- Day19 provides the retrieval layer and feature-serving layer through hybrid search and Feast.
- Day20 provides the final serving layer through an OpenAI-compatible local inference endpoint.

The final live demo focuses on the serving path that can be run on the local machine:

Day19 hybrid retrieval -> Day20 prompt assembly -> Day20 llama-server answer.

## Deployment note

Day16 used GCP infrastructure and Terraform evidence. Day20 serving is demonstrated locally on the NVIDIA RTX 4060 Laptop GPU because the GCP project did not have available GPU quota. This is documented as a CPU/cloud fallback plus local GPU serving split.

## Files connected to this architecture

- `MILESTONE1.md`
- `integration/end_to_end_demo.md`
- `integration/runbook.md`
- `benchmarks/milestone1-latency-cost.md`
- `03-milestone-integration/pipeline.py`
- `benchmarks/03-real-integration-summary.md`
- `benchmarks/03-real-rag-pipeline-output.txt`
