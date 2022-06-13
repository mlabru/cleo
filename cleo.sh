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
    docker-compose up -d &
    # wait 15s
    sleep 15s
fi

# ckeck if another instance of worker is running
DI_PID_WORKER=`ps ax | grep -w python3 | grep -w worker.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_WORKER" ]; then
    # log warning
    echo "[`date`]: process worker is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_WORKER
    # wait 3s
    sleep 3
fi

# set PYTHONPATH
export PYTHONPATH="$PWD/."

# log warning
echo "[`date`]: starting process worker..."
# executa o worker (message queue consumer)
python3 cleo/worker.py > logs/worker.$HOST.$TDATE.log 2>&1 &

# ckeck if another instance os cleo is running
DI_PID_CLEO=`ps ax | grep -w streamlit | grep -w st_cleo.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_CLEO" ]; then
    # log warning
    echo "[`date`]: process cleo is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_CLEO
    # wait 3s
    sleep 3
fi

# log warning
echo "[`date`]: starting process cleo..."
# executa a aplicação (-OO)
streamlit run cleo/st_cleo.py > logs/st_cleo.$HOST.$TDATE.log 2>&1 &

# < the end >----------------------------------------------------------------------------------
