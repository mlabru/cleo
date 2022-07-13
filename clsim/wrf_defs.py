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

# < servidor FTP >-----------------------------------------------------------------------------

# File server IP
DS_FS_HOST = os.getenv("DS_FS_HOST")
# File server port
DI_FS_PORT = os.getenv("DI_FS_PORT")

# < servidor SMTP >----------------------------------------------------------------------------

# SMTP host address
DS_SMTP_SERVER = os.getenv("DS_SMTP_SERVER")
# SMTP normal port
DI_SMTP_PORT = os.getenv("DI_SMTP_PORT")
# SMTP SSL port
# DI_SMTP_SSL_PORT = os.getenv("DI_SMTP_SSL_PORT")

# SMTP password
DS_SMTP_PWD = os.getenv("DS_SMTP_PWD")
# SMTP user
DS_SMTP_USR = os.getenv("DS_SMTP_USR")

# email from
DS_EMAIL_FROM = os.getenv("DS_EMAIL_FROM")
# email developer
DS_EMAIL_DEVL = os.getenv("DS_EMAIL_DEVL")
# email meteoro
DS_EMAIL_WRF = os.getenv("DS_EMAIL_WRF")

# < defines >----------------------------------------------------------------------------------

# email message template
DS_EMAIL_BODY_OK = string.Template("""
Segue o link com o resultado da simulação: ($xtok)

$xlink.

Este arquivo estará disponível por 7 dias a contar da data de envio deste e-mail.

""")

# email error message template
DS_EMAIL_BODY_ERR = string.Template("""
Ocorreu o seguite erro na simulação: ($xtok)

$xmsg.

""")

# FTP download URL
DS_FTP_URL = f"http://{DS_FS_HOST}:{DI_FS_PORT}/shared/clsim/"

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
