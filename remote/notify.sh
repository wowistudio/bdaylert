#!/bin/bash

export PYTHONUNBUFFERED=1
export PYTHONPATH=/root/bday/src

cd /root/bday
export $(cat .env | xargs) >/dev/null
source venv/bin/activate
python3 src/bday/notify.py