#!/bin/bash
cd "${0%/*}"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pywright install chromium
deactivate
