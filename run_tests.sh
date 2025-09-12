#!/bin/bash

echo "Running unit tests..."
pytest tests/unit/ -v

echo "Running integration tests..."
pytest tests/integration/ -v

echo "Running E2E tests..."
pytest tests/e2e/ -v

echo "Test coverage report:"
pytest --cov=src --cov-report=html