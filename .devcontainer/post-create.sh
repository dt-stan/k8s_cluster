#!/bin/bash

# Initialize Kind Cluster
kind create cluster --config .devcontainer/kind-cluster.yaml --wait 180s
