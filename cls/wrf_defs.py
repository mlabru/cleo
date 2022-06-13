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

# FTP server IP
DS_FTP_HOST = os.getenv("DS_FTP_HOST")
# FTP server port
DI_FTP_PORT = os.getenv("DI_FTP_PORT")
# FTP server user
DS_FTP_USER = os.getenv("DS_FTP_USER")
# FTP server password
DS_FTP_PASS = os.getenv("DS_FTP_PASS")

# < servidor SMTP >----------------------------------------------------------------------------

# SMTP host address
DS_SMTP_SERVER = os.getenv("DS_SMTP_SERVER")
# SMTP normal port
DI_SMTP_PORT = os.getenv("DI_SMTP_PORT")
# SMTP SSL port
DI_SMTP_SSL_PORT = os.getenv("DI_SMTP_SSL_PORT")

# SMTP app password
DS_SMTP_APP_PWD = os.getenv("DS_SMTP_APP_PWD")
# SMTP user
DS_SMTP_USR = os.getenv("DS_SMTP_USR")

# email from
DS_EMAIL_FROM = os.getenv("DS_EMAIL_FROM")
# email admin
DS_EMAIL_ADMIN = os.getenv("DS_EMAIL_ADMIN")

# < defines >----------------------------------------------------------------------------------

# email message template
DS_EMAIL_BODY_OK = string.Template("""
Segue o link com o resultado da simulação:
$xlink.

Este arquivo estará disponível por 7 dias a contar da data de envio deste e-mail.

Obs: O Chrome removeu o suporte a FTP recentemente.  Você poderá reativá-lo
se tiver a versão 88 ou anterior.  Espera-se a versão 89 remova todo o
código FTP.  Você poderá usar o Firefox, wget ou um aplicativo, como WSFTP
ou similar.
""")

# email error message template
DS_EMAIL_BODY_ERR = string.Template("""
Ocorreu o seguite erro na simulação ($xtok):
$xmsg.
""")

# FTP download URL
DS_FTP_URL = f"ftp://{DS_FTP_USER}:{DS_FTP_PASS}@{DS_FTP_HOST}:{DI_FTP_PORT}/"

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
