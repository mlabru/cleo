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
import email
import glob
import json
import logging
import os
import pathlib
import subprocess
import sys
import time

# local
import cls.cls_defs as df
import cls.wrf_defs as wdf
import cls.wrk_email as wem

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

    # build link
    # ex: ftp://<user>:<pass>@<host>:<port>/<dir>/201204110048BR6.tgz
    ls_link = "{}{}{:02d}{:02d}{}{:02d}{}.tgz".format(wdf.DS_FTP_URL,
                                                      ldct_parms["year"],
                                                      ldct_parms["month"],
                                                      ldct_parms["day"],
                                                      ldct_parms["hora"],
                                                      ldct_parms["delta"],
                                                      ldct_parms["regiao"])

    # exec WRF process
    try:
        # exec WRF
        # subprocess.run(["bash", wdf.DS_BASH_WRF, ls_parms], capture_output=True, check=True)
        M_LOG.debug("subprocess.run: %s", str(["bash", str(wdf.DS_BASH_WRF), ls_parms]))

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = ldct_parms["email"].strip()
        l_email["subject"] = "CLSim - Resultado da Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_OK.substitute(xlink=ls_link))

        # send confirmation e-mail
        wem.send_message(ldct_parms["email"].strip(), l_email.as_string())

        # remove token
        pathlib.Path.unlink(pathlib.Path(fs_config))

    # em caso de erro...
    except subprocess.CalledProcessError as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (1): %s", str(lerr.output.decode()))

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = wdf.DS_EMAIL_FROM
        l_email["subject"] = "CLSim - Erro na Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_OK.substitute(xlink=ls_link,
                                                            xmsg=lerr.output.decode()))

        # enviar mail com aviso de erro para o usuário
        wem.send_message(wdf.DS_EMAIL_FROM, l_email.as_string())

    # em caso de erro...
    except Exception as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (2): %s", str(lerr))

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = wdf.DS_EMAIL_ADMIN
        l_email["subject"] = "CLSim - Erro na Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_OK.substitute(xlink=ls_link,
                                                            xmsg=str(lerr)))

        # enviar mail com aviso de erro para o usuário
        wem.send_message(wdf.DS_EMAIL_ADMIN, l_email.as_string())

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
        llst_files = glob.glob(os.path.join(wdf.DS_DIR_JOBS, "*.json"))
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
