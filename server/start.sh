#!/bin/bash

REL_SCRIPT_PATH="${BASH_SOURCE[0]}"
REL_SCRIPT_DIR="$(dirname $REL_SCRIPT_PATH)"
ABS_SCRIPT_DIR="$(cd $REL_SCRIPT_DIR && pwd)"
cd $ABS_SCRIPT_DIR


pip install -r requirements.txt

gunicorn -b 0.0.0.0:9001 app.main --workers 10 --timeout 600
