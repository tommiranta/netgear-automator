#!/bin/bash
cd "${0%/*}"
source venv/bin/activate
python main.py $1
deactivate
