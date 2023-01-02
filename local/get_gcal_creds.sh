#!/bin/bash

envfile=$(dirname $(realpath $0))/.env
export $(cat $envfile | xargs) > /dev/null
export PYTHONPATH=$(dirname $(realpath $0))/../src

python -c 'from bday.gcal.authorize import authorize; authorize()'