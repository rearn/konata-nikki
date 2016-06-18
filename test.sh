#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)
export PY=python3

$PY -m unittest discover -s tests/ $@
