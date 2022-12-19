#!/usr/bin/env bash

set -eEuxo pipefail

# make root folder
d="/root/bday"
ssh bday mkdir -p "$d"

## copy folders with code
scp -r src "bday:$d"
scp -r remote "bday:$d"
scp remote/.bashrc bday:~/.bashrc

## install python requirements
scp -r requirements "bday:$d"
ssh bday << EOF
  cd $d
  [[ ! -d venv ]] && python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements/base.txt
  'find bday -name __pycache__ -exec rm -r \{\} \;' &>/dev/null || true
EOF

## start service
scp remote/bday.service bday:/etc/systemd/system
ssh bday 'chmod 664 /etc/systemd/system/bday.service'
ssh bday "chmod +x $d/remote/start.sh"

ssh bday 'systemctl daemon-reload'
ssh bday 'systemctl start bday'
ssh bday 'systemctl status bday'
