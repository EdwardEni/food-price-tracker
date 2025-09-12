#!/bin/bash

echo "Running basic tests..."
pytest tests/unit/test_basic.py -v

echo "Running scraper tests..."
pytest tests/unit/test_scraper.py -v

echo "Running alert tests..."
pytest tests/unit/test_alerts.py -v

echo "Test completed!"