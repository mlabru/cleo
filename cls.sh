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

# ckeck if another instance of worker is running
DI_PID_WRK=`ps ax | grep -w python3 | grep -w worker.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_WRK" ]; then
    # log warning
    echo "[`date`]: process worker is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_WRK
    # wait 3s
    sleep 3
fi

# set PYTHONPATH
export PYTHONPATH="$PWD/."

# log warning
echo "[`date`]: starting process worker..."
# executa o worker (message queue consumer)
python3 cls/worker.py > logs/worker.$HOST.$TDATE.log 2>&1 &

# ckeck if another instance os cls is running
DI_PID_CLS=`ps ax | grep -w streamlit | grep -w st_cls.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_CLS" ]; then
    # log warning
    echo "[`date`]: process cls is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_CLS
    # wait 3s
    sleep 3
fi

# log warning
echo "[`date`]: starting process cls..."
# executa a aplicação (-OO)
streamlit run cls/st_cls.py > logs/st_cls.$HOST.$TDATE.log 2>&1 &

# < the end >----------------------------------------------------------------------------------
