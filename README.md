# docker-k8s-practice

Hands-on practice with Docker, Kubernetes and CI/CD. A small Flask API is
containerized, run locally with Docker Compose, deployed to a local Kubernetes
cluster (kind), and verified by a GitHub Actions pipeline that also publishes the
image to GitHub Container Registry.

## What it demonstrates

- Dockerfile with layer caching, non-root user and a health check.
- Docker Compose for local development.
- Kubernetes manifests: Namespace, ConfigMap, Deployment (2 replicas, rolling
  update, readiness and liveness probes, resource requests and limits) and Service.
- CI pipeline: unit tests, image build, deploy to an ephemeral kind cluster with a
  smoke test, and image publishing to GHCR on `main`.

## Run it

```bash
# Docker
docker build -t practica-app:local .
docker run --rm -p 8000:8000 practica-app:local
curl localhost:8000/health

# Docker Compose
docker compose up --build

# Kubernetes (kind)
kind create cluster --name practica
kind load docker-image practica-app:local --name practica
kubectl apply -f k8s/
kubectl -n practica get pods
kubectl -n practica port-forward svc/practica-app 8080:80
curl localhost:8080/
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Structure

```
app/            Flask application
tests/          unit tests
Dockerfile      container image
docker-compose.yml
k8s/            Kubernetes manifests
.github/workflows/ci.yml
docs/GUIA_PRACTICA.md   step-by-step practice guide (Spanish)
```
