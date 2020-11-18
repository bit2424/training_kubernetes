#!/bin/bash
export PYTHONPATH=$PYTHONPATH:`pwd`

LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
PORT=5000

if [[ -z $PRODUCTION ]]
then
  export FLASK_ENV=development
fi

python ./src/launch.py 