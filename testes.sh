#!/bin/bash
set -e

mypy src/
python -m unittest discover -s tests
