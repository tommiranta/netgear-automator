#!/bin/bash
cd "${0%/*}"
source venv/bin/activate
source .env
echo "`date` Run script with value: $1"
python main.py $1
deactivate
