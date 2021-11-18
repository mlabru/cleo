#!/bin/bash

# language
# export LANGUAGE=pt_BR

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# home directory exists ?
if [ -d "/home/webpca/clsim/cleo" ]; then
    # set home dir
    cd /home/webpca/clsim/cleo
fi

# executa a aplicação (-OO)
streamlit run cleo.py > logs/cleo.$HOST.$TDATE.log 2>&1 &
