#!/bin/bash

REL_SCRIPT_PATH="${BASH_SOURCE[0]}"
REL_SCRIPT_DIR="$(dirname $REL_SCRIPT_PATH)"
ABS_SCRIPT_DIR="$(cd $REL_SCRIPT_DIR && pwd)"
cd $ABS_SCRIPT_DIR


gunicorn -b 0.0.0.0:9001 main
