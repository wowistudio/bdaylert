#!/bin/bash

export PYTHONUNBUFFERED=1
export PYTHONPATH=/root/bday/src
export DOTENV_FILE=/root/bday/.env

cd /root/bday
source venv/bin/activate
python3 src/bday/main.py