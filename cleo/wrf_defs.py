# -*- coding: utf-8 -*-
"""
wrf_defs

2021.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import pathlib

# dotenv
import dotenv

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# < defines >----------------------------------------------------------------------------------

# source path
DS_SRC_PATH = pathlib.Path(__file__).resolve().parent.parent

# execWRF batch
DS_BASH_WRF = pathlib.PurePath(DS_SRC_PATH, "execWRF.sh")

# lista de regiões
DLST_REGIAO_NOME = ["Norte", "Sudeste", "Brasília - mp6", "Brasília - mp10"]

# lista de siglas de regiões
DLST_REGIAO_SIGLA = ["N", "SE", "BR6", "BR10"]

# < the end >----------------------------------------------------------------------------------
