#!/bin/bash

# language
# export LANGUAGE=pt_BR

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# get all command line arguments
CMDLIN=( $@ )

# length of array
CLLEN=${#CMDLIN[@]}

# email
EMAIL=${CMDLIN[$CLLEN-1]}

# parameters (região, data ini, data fim)
PARMS=${CMDLIN[@]:0:$CLLEN-1}

# token (parameters sem espaços)
TOKEN="$(echo -e "${PARMS}" | tr -d '[:space:]')"

# home dir do execWRF
cd ~/clsim/execWRF

echo "Token: $TOKEN / Parms: $PARMS / E-mail: $EMAIL"

# executa a aplicação
python3 exec_wrf.py $@ > ~/clsim/cleo/logs/logWRF.$TOKEN.log 2>&1
