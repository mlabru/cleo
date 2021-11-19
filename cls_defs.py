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
DI_LOG_LEVEL = logging.DEBUG
# DI_LOG_LEVEL = logging.WARNING

# lista de regiões
DLST_REGIAO_NOME = ["Norte", "Sudeste"]
DLST_REGIAO_SIGLA = ["N", "SE"]

# RabbitMQ server
DS_MSQ_SRV = "localhost"
# DS_MSQ_SRV = "172.18.30.30"

# -------------------------------------------------------------------------------------------------
import imp

# open secrets files
with open(".hidden/cls_secrets.py", "rb") as lfh:
    # import module
    hs = imp.load_module(".hidden", lfh, ".hidden/cls_secrets", (".py", "rb", imp.PY_SOURCE))

# < the end >--------------------------------------------------------------------------------------
