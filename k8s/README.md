# Kubernetes Deployment Note

## Purpose

This folder documents how the Milestone 1 platform would be deployed on Kubernetes in a production setting.

The actual live demo runs locally in WSL because:

- Day16 cloud GPU provisioning was blocked by zero GCP GPU quota.
- Day20 model serving was successfully demonstrated on the local NVIDIA RTX 4060 Laptop GPU.
- The goal of the live demo is to prove the end-to-end integration path, not to incur cloud GPU cost.

## Production mapping

| Component | Kubernetes equivalent |
|---|---|
| Day19 FastAPI search API | Deployment + Service on port 8000 |
| Day19 Qdrant | StatefulSet or managed vector database |
| Day19 Redis online store | StatefulSet or managed Redis |
| Day20 llama-server | GPU Deployment + Service on port 8080 |
| Metrics | Prometheus scrape endpoint |
| Routing | Ingress / Gateway API |
| Autoscaling | KEDA / HPA based on queue depth, GPU utilization, or request rate |

## Live demo mapping

The live demo uses local services:

| Local service | Port |
|---|---:|
| Day19 FastAPI `/search` | 8000 |
| Day20 llama-server `/v1/chat/completions` | 8080 |

This is equivalent to the Kubernetes service-to-service path:

Day20 pipeline -> Day19 search service -> Day20 llama-server service.

## Future production steps

1. Containerize Day19 API.
2. Containerize Day20 llama-server with the selected GGUF model mounted as a volume.
3. Create Kubernetes Deployments and Services.
4. Add GPU node selectors for Day20 serving.
5. Add Prometheus scraping for `/metrics`.
6. Add KEDA/HPA autoscaling based on queue depth and GPU utilization.
7. Add Ingress/Gateway for external access.
8. Add persistent storage for vector DB, feature store, and model artifacts.
