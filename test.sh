#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)
export PY=python3

$PY tests/test_konata.py $@
