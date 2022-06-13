# -*- coding: utf-8 -*-
"""
wrf_defs

2021.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import os
import pathlib
import string

# dotenv
import dotenv

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# SMTP host address
DS_SMTP_SERVER = os.getenv("DS_SMTP_SERVER")
# SMTP normal port
DI_SMTP_PORT = os.getenv("DI_SMTP_PORT")
# SMTP SSL port
DI_SMTP_SSL_PORT = os.getenv("DI_SMTP_SSL_PORT")

# SMTP user
DS_SMTP_USR = os.getenv("DS_SMTP_USR")
# SMTP app password
DS_SMTP_APP_PWD = os.getenv("DS_SMTP_APP_PWD")

# email from
DS_EMAIL_FROM = os.getenv("DS_EMAIL_FROM")

# email message template
DS_EMAIL_BODY_OK = string.Template("""
From: $xfrom
To: $xto
Subject: CLSim - Resultado da Simulação

Segue o link com o resultado da simulação:
$xlink.
""")

# email error message template
DS_EMAIL_BODY_ERR = string.Template("""
From: $xfrom
To: $xto
Subject: CLSim - Erro na Simulação

Ocorreu o seguite erro na simulação ($xtok):
$xmsg.
""")

# < defines >----------------------------------------------------------------------------------

# source path
DS_SRC_PATH = pathlib.Path(__file__).resolve().parent.parent

# execWRF batch
DS_BASH_WRF = pathlib.PurePath(DS_SRC_PATH, "execWRF.sh")

# jobs directory
DS_DIR_JOBS = pathlib.PurePath(DS_SRC_PATH, "jobs")

# lista de regiões
DLST_REGIAO_NOME = ["Norte", "Sudeste", "Brasília - mp6", "Brasília - mp10"]

# lista de siglas de regiões
DLST_REGIAO_SIGLA = ["N", "SE", "BR6", "BR10"]

# simulation result upload
DV_RESULT_UPLOAD = False

# < the end >----------------------------------------------------------------------------------
