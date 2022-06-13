# -*- coding: utf-8 -*-
"""
cleo_defs

2021.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import pathlib

# dotenv
import dotenv

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# < defines >----------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.DEBUG

# source path
DS_SRC_PATH = pathlib.Path(__file__).resolve().parent.parent

# jobs directory
DS_DIR_JOBS = pathlib.PurePath(DS_SRC_PATH, "jobs")

# simulation result upload
DV_RESULT_UPLOAD = False

# < the end >----------------------------------------------------------------------------------
