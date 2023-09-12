#!/bin/bash
cd "${0%/*}"
source venv/bin/activate
echo "`date` Run script with value: $1"
python main.py $1
deactivate
