# Milestone 1 Live Demo Runbook

## Pre-demo checklist

Run from Day20 repo:

    cd /home/emin98/labs/Day20-Track2-ModelServing-Lab
    git status
    ls MILESTONE1.md architecture/milestone1-architecture.md integration/end_to_end_demo.md benchmarks/milestone1-latency-cost.md

Confirm the required evidence files exist:

    ls benchmarks/03-real-integration-summary.md
    ls benchmarks/03-real-rag-pipeline-output.txt
    ls submission/screenshots/07-real-rag-pipeline.png

## Start Day19

In Terminal 1:

    cd /home/emin98/labs/Day19-Track2-VectorFeatureStore-Lab
    docker compose up -d
    make api

Check:

    curl http://localhost:8000/healthz
    curl "http://localhost:8000/search?q=cloud%20autoscaling&mode=hybrid&top_k=3"

## Start Day20

In Terminal 2:

    cd /home/emin98/labs/Day20-Track2-ModelServing-Lab
    make serve

Check from Terminal 3:

    curl http://localhost:8080/v1/models

## Run demo

In Terminal 3:

    cd /home/emin98/labs/Day20-Track2-ModelServing-Lab
    python 03-milestone-integration/pipeline.py

## What to say during the demo

1. This is the final Milestone 1 integration across N16 to N20.
2. Day16 provides cloud/IaC evidence through Terraform on GCP.
3. Day17 provides the data pipeline and validation layer.
4. Day18 provides the Delta Lakehouse and Medallion architecture.
5. Day19 provides vector retrieval and feature store services.
6. Day20 provides model serving and benchmark evidence.
7. The live path being executed now is Day19 hybrid retrieval into Day20 llama-server.
8. The printed context IDs prove retrieval is coming from Day19.
9. The printed timings show retrieval, LLM, and total latency.

## Failure handling

If Day19 fails:

- Check that port 8000 is running.
- Re-run `docker compose up -d`.
- Re-run `make api`.
- Test `/healthz` and `/search`.

If Day20 fails:

- Check that port 8080 is running.
- Re-run `make serve`.
- Test `/v1/models`.

If the pipeline returns no hits:

- Lower query specificity.
- Confirm Day19 data is seeded/indexed.
- Test Day19 `/search` directly.

If llama-server is slow:

- Explain that this is a local laptop GPU demo.
- Use the benchmark report to discuss P50/P95/P99 and Locust results.
