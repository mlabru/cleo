#!/bin/bash

# language
# export LANGUAGE=pt_BR

# cleo directory
CLEO=~/clsim/cleo

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# home directory exists ?
if [ -d ${CLEO} ]; then
    # set home dir
    cd ${CLEO}
fi

# executa a aplicação (-OO)
python3 wrk_160.py > logs/wrk_160.$HOST.$TDATE.log 2>&1 &
