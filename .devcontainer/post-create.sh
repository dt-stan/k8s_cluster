#!/bin/bash

# Configure Poetry for devcontainer
poetry config virtualenvs.create false
poetry install --project ./src

# Initialize Kind Cluster
kind create cluster --config .devcontainer/kind-cluster.yaml --wait 180s
