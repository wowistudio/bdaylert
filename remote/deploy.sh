#!/usr/bin/env bash

set -eEuxo pipefail

# make root folder
d="/root/bday"
ssh jeroen mkdir -p "$d"

## copy folders with code
scp -r src "jeroen:$d"
scp -r remote "jeroen:$d"
scp ./local/.env jeroen:$d
scp remote/.bashrc jeroen:~/.bashrc

# cron
echo "* 7 * * * /root/bday/remote/notify.sh" | ssh jeroen "crontab -"

## install python requirements
scp -r requirements "jeroen:$d"
ssh jeroen << EOF
  echo "HELLO"
  cd $d
  apt -y install python3.10-venv
  [[ ! -d venv ]] && python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements/base.txt
  'find jeroen -name __pycache__ -exec rm -r \{\} \;' &>/dev/null || true
EOF

# allow notify

# start service
ssh jeroen "chmod +x $d/remote/notify.sh"
scp remote/bday.service jeroen:/etc/systemd/system
ssh jeroen 'chmod 664 /etc/systemd/system/bday.service'
ssh jeroen "chmod +x $d/remote/start.sh"

ssh jeroen 'systemctl daemon-reload'
ssh jeroen 'systemctl start bday'
ssh jeroen 'systemctl status bday'
