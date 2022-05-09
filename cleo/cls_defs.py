# -*- coding: utf-8 -*-
"""
cls_defs

2021/may  1.0  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# < defines >----------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.DEBUG
# DI_LOG_LEVEL = logging.WARNING

# lista de regiões
DLST_REGIAO_NOME = ["Norte", "Sudeste", "Brasília - mp6", "Brasília - mp10"]
DLST_REGIAO_SIGLA = ["N", "SE", "BR6", "BR10" ]

# RabbitMQ server
DS_MSQ_SRV = "localhost"
# DS_MSQ_SRV = "172.18.30.160"

# RabbitMQ queue
DS_MSQ_QUEUE = "execWRF"

# simulation result upload
DV_RESULT_UPLOAD = False

# < the end >----------------------------------------------------------------------------------
