#!/usr/bin/env bash
## testing
python -m unittest tests/test_profiler.py

## build
python setup.py bdist_wheel

## deploy
cp dist/pycronicle-*.whl ../../prod/cronicle/dist

## clean all
python setup.py clean --all
rm -rf data