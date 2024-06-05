#!/usr/bin/env bash

# stop at first error
set -e

python -W ignore ./left_turn.py
python -W ignore ./left_turn_tests.py

