# -*- coding: utf-8 -*-
"""
cleo_defs

2021.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# < defines >----------------------------------------------------------------------------------

# logging level
# DI_LOG_LEVEL = logging.DEBUG
DI_LOG_LEVEL = logging.WARNING

# RabbitMQ server
DS_MSQ_SRV = "localhost"
# DS_MSQ_SRV = "172.18.30.175"

# RabbitMQ queue
DS_MSQ_QUEUE = "execWRF"

# simulation result upload
DV_RESULT_UPLOAD = False

# < the end >----------------------------------------------------------------------------------
