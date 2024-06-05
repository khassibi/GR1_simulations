#!/usr/bin/env bash
# stop at first error
set -e

python -W ignore ./Tgame.py
python -W ignore ./Tgame_tests.py
