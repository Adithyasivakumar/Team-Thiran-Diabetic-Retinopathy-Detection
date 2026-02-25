#!/bin/bash
#
# Team Thiran - DR Detection System
# Start script for the application
#
# Usage: ./run.sh

cd "$(dirname "$0")"
python3 frontend/blindness.py
