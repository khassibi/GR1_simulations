#!/usr/bin/env bash
# cd /Users/kimiahassibi/Desktop/Caltech/SURF2023/GR1_simulations/left_turn_pedestrian
# find . -type f ! \( -name 'StatesExplained.png' -o -name 'create_tests.sh -o -name '__init__.py' \) -exec rm {} \;
# stop at first error
set -e

python -W ignore ./left_turn_pedestrian.py
python -W ignore ./left_turn_pedestrian_tests.py

