#!/usr/bin/env sh
set -eu
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/src"
pytest
python simulation/red_team_campaign.py
python benchmarks/run_benchmarks.py
python test_vectors/generate_vectors.py
