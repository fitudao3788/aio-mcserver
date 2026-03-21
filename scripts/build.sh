#!/bin/bash

python -m nuitka --standalone --onefile --output-dir=$(dirname $0)/../dist $(dirname $0)/../main.py
