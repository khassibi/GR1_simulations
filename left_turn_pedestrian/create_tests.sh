#!/usr/bin/env bash
# stop at first error
set -e

python -W ignore ./left_turn_pedestrian.py
python -W ignore ./left_turn_pedestrian_tests.py

