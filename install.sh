#!/bin/bash
cd "${0%/*}"

echo "Creating virtual environment"
python -m venv venv
source venv/bin/activate

echo "Installing required packages"
pip install -r requirements.txt
deactivate
