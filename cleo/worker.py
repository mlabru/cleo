# -*- coding: utf-8 -*-
"""
worker
work queue consumer

2022.jun  mlabru  remove rabbitmq cause of timeout problems, remove graylog
2022.may  mlabru  melhorias no try...except
2022.apr  mlabru  graylog log management
2021.nov  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import glob
import json
import logging
import os
import pathlib
import subprocess
import sys
import time

# local
import cleo.cleo_defs as df
import cleo.wrf_defs as wdf
# import cleo.wrk_email as wem

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def exec_job(fs_config: pathlib.Path):
    """
    process messages

    :param fs_config: job config file
    """
    # logger
    M_LOG.info("exec_job >>")

    # parâmetros do job
    ldct_parms = {}

    # load JSON config file
    with open(fs_config, 'r') as fhd:
        # get parameters
        ldct_parms = json.load(fhd)

    # build dos parâmetros de entrada
    # ex: <AAAA> <MM> <DD> <INÍCIO> <TEMPO> <REGIÃO> [E-MAIL]
    ls_parms = "{} {:02d} {:02d} {} {:02d} {} {}".format(ldct_parms["year"],
                                                         ldct_parms["month"],
                                                         ldct_parms["day"],
                                                         ldct_parms["hora"],
                                                         ldct_parms["delta"],
                                                         ldct_parms["regiao"],
                                                         ldct_parms["email"])

    try:
        # exec WRF
        # subprocess.run(["bash", wdf.DS_BASH_WRF, ls_parms], capture_output=True, check=True)
        M_LOG.debug("subprocess.run: %s", str(["bash", str(wdf.DS_BASH_WRF), ls_parms]))

        # send confirmation e-mail
        # wem.send_email(llst_parms[-1].strip(), ls_token, False)

        # remove token
        pathlib.Path.unlink(pathlib.Path(fs_config))

    # em caso de erro...
    except subprocess.CalledProcessError as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (1): %s", str(lerr.output.decode()))
    
        # TODO:
        # enviar mail com aviso de erro para o usuário.
        # wem.send_email(llst_parms[-1].strip(), ls_token, False)

    # em caso de erro...
    except Exception as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (2): %s", str(lerr))

        # TODO:
        # enviar mail com aviso de erro para o usuário.
        # wem.send_email(llst_parms[-1].strip(), ls_token, False)

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.info("main >>")

    # logger
    M_LOG.info(" [*] Waiting for messages. To exit press CTRL+C")

    # forever...
    while True:
        # list of all files in directory sorted by name
        llst_files = glob.glob(os.path.join(df.DS_DIR_JOBS, "*.json"))
        # list of all files in directory sorted by name
        llst_files = sorted(filter(os.path.isfile, llst_files))
              
        # tem jobs na fila ?
        if llst_files:
            # logger
            M_LOG.info(" [x] Received %s", str(llst_files[0]))

            # process job
            exec_job(llst_files[0])

        # senão,...
        else: 
            # allows task switch
            time.sleep(30)
        
# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%Y/%m/%d %H:%M",
                        format="%(asctime)s %(message)s",
                        level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxsize)

    try:
        # run application
        main()

    # em caso de erro...
    except KeyboardInterrupt:
        # logger
        logging.warning("Interrupted.")

    # terminate
    sys.exit(0)

# < the end >----------------------------------------------------------------------------------
