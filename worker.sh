#!/bin/bash

# language
# export LANGUAGE=pt_BR

# CLSim directory
CLSIM=~/clsim

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# home directory exists ?
if [ -d ${CLSIM} ]; then
    # set home dir
    cd ${CLSIM}
fi

# rabbitMQ container not loaded ?
if ! [ "$( docker container inspect -f '{{.State.Running}}' rabbitmq )" == "true" ]; then
    # upload rabbitmq
    sudo docker-compose up -d &
fi

# executa a aplicação (-OO)
python3 cleo/worker.py > logs/worker.$HOST.$TDATE.log 2>&1 &
