#!/bin/bash

# language
# export LANGUAGE=pt_BR

# nome do computador
HOST=`hostname`
echo ${HOST}

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`
echo "TDATE" ${TDATE}

echo "args: " $@

# get all command line arguments
CMDLIN=( $@ )
echo "CMDLIN" ${CMDLIN[@]}

# length of an array
CLLEN=${#CMDLIN[@]}
echo "CLLEN" ${CLLEN}

# email
EMAIL=${CMDLIN[$CLLEN-1]}
echo "EMAIL" ${EMAIL}

# parameters (região, data ini, data fim)
PARMS=${CMDLIN[@]:0:$CLLEN-1}
echo "PARMS" ${PARMS}

# token (parameters sem espaços)
TOKEN="$(echo -e "${PARMS}" | tr -d '[:space:]')"
echo "TOKEN" ${TOKEN}

# home dir do WRF
cd /home/webpca/WRF

# executa a aplicação
bash ./runWRF.sh $@ > /home/webpca/clsim/cleo/logs/logWRF.$TOKEN.log 2>&1
