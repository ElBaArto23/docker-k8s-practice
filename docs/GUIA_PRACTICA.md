# Guía de práctica: Docker y Kubernetes

Ruta sugerida en 3 sesiones. Todo corre gratis en tu computador. No hace falta Azure.

## Requisitos

- Docker (Docker Desktop, o Docker Engine en Linux/WSL2). Prueba con `docker version`.
- `kubectl` y `kind`. Prueba con `kubectl version --client` y `kind version`.
- Git y Python 3.12 (solo para correr los tests en local).

## Sesión 1: Docker (1 a 1,5 h)

1. Ejecuta los tests: `pip install -r requirements-dev.txt && pytest`.
2. Construye la imagen: `docker build -t practica-app:local .`
3. Córrela: `docker run --rm -p 8000:8000 practica-app:local` y abre `localhost:8000`.
4. Explora: `docker ps`, `docker logs <id>`, `docker exec -it <id> sh`, `docker images`.
5. Vuelve a construir sin cambiar nada y fíjate en que usa la caché. Cambia `app.py` y mira qué capas se reconstruyen.
6. Levanta con Compose: `docker compose up --build` y luego `docker compose down`.

Ejercicios:
- Cambia el mensaje con una variable: `docker run -e GREETING="Hola Yackson" ...`
- Compara el tamaño de `python:3.12-slim` con `python:3.12` y explica la diferencia.
- Confirma que el contenedor no corre como root: `docker exec <id> whoami`.

## Sesión 2: Kubernetes en local con kind (1,5 a 2 h)

1. Crea el clúster: `kind create cluster --name practica`
2. Carga la imagen: `kind load docker-image practica-app:local --name practica`
3. Aplica los manifiestos: `kubectl apply -f k8s/`
4. Mira los recursos: `kubectl -n practica get all`
5. Accede: `kubectl -n practica port-forward svc/practica-app 8080:80`
6. Inspecciona: `kubectl -n practica describe pod <pod>` y `kubectl -n practica logs <pod>`.

Ejercicios (los que más enseñan):
- **Escalar:** `kubectl -n practica scale deployment/practica-app --replicas=4`. Llama varias veces a `/` y mira cómo cambia el `hostname`.
- **Auto-recuperación:** borra un pod con `kubectl -n practica delete pod <pod>` y mira cómo se crea otro.
- **Actualización progresiva:** cambia `APP_VERSION` en `10-configmap.yaml` y en el código, reconstruye la imagen con otra etiqueta (`practica-app:v2`), carga la imagen y actualiza con `kubectl -n practica set image deployment/practica-app web=practica-app:v2`. Observa con `kubectl -n practica rollout status deployment/practica-app` y revierte con `kubectl -n practica rollout undo deployment/practica-app`.
- **Romper las sondas:** cambia la ruta de `readinessProbe` a `/nada` y mira por qué los pods no quedan `Ready`.
- **Configuración:** edita el ConfigMap, reaplica y reinicia con `kubectl -n practica rollout restart deployment/practica-app`.
- **Límites de recursos:** baja el límite de memoria a `10Mi` y observa el `OOMKilled`.

Limpieza: `kind delete cluster --name practica`

## Sesión 3: Pipeline (1 h)

1. Sube el proyecto a un repositorio nuevo de GitHub.
2. Mira la pestaña Actions: deben correr `test`, `k8s-smoke-test` y, en `main`, `publish`.
3. Rompe algo a propósito (por ejemplo, la ruta `/health`) y comprueba que el pipeline se pone en rojo y qué información de depuración imprime.
4. Revisa en tu perfil de GitHub, sección Packages, la imagen publicada en GHCR.

## Cuándo ponerlo en el CV

Cuando hayas hecho las tres sesiones y el pipeline esté en verde. Una redacción posible (ajústala a lo que hiciste):

> Proyecto de contenedores y orquestación: API en Python empaquetada con Docker (usuario no root, health check) y desplegada en Kubernetes (Deployment con 2 réplicas, sondas, límites de recursos, actualizaciones progresivas). Pipeline en GitHub Actions que ejecuta pruebas, despliega en un clúster kind efímero con prueba de humo y publica la imagen en GitHub Container Registry.

Habilidades: Docker, Docker Compose, Kubernetes, kubectl, GitHub Actions, CI/CD, GHCR.

## Siguiente nivel

- Ingress con NGINX en kind.
- Helm: convertir `k8s/` en un chart.
- Terraform: desplegar la misma imagen en AKS cuando abras la cuenta de Azure.
- Escribir commits y comentarios en inglés para practicar.
