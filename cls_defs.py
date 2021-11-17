# -*- coding: utf-8 -*-
"""
cls_defs

2021/may  1.0  mlabru  initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < defines >--------------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.WARNING
# DI_LOG_LEVEL = logging.DEBUG

# lista de regiões
DLST_REGIAO_NOME = ["Norte", "Sudeste"]
DLST_REGIAO_SIGLA = ["N", "SE"]

# RabbitMQ server
DS_MSGQ_SRV = "172.18.30.30"

# message queue user/passwd
DS_USER = "clsim"
DS_PASS = "segredo"

# intervalo máximo de previsão em horas
DI_DELTA = 48

# < the end >--------------------------------------------------------------------------------------
