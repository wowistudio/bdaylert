#!/bin/bash

export PYTHONPATH=$(dirname $(realpath $0))/../src
python -c 'from bday.gcal.authorize import authorize; authorize()'