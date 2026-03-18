#!/usr/bin/env sh

set -eu

PROFILE="${PROFILE:-aeroporto}"
IMAGE="${IMAGE:-aeroporto-backend:latest}"

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BACKEND_DIR="$ROOT_DIR/backend"

minikube start --driver=docker --profile "$PROFILE"
docker build -t "$IMAGE" "$BACKEND_DIR"
minikube image load "$IMAGE" --profile "$PROFILE"
kubectl apply -k "$ROOT_DIR/k8s"
