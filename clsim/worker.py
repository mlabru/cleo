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
import clsim.cls_defs as df
import clsim.wrf_defs as wdf
import clsim.wrk_email as wem

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def exec_job(f_job_cfg: pathlib.Path):
    """
    process messages

    :param f_job_cfg: job config file
    """
    # logger
    M_LOG.info("exec_job >>")

    # parâmetros do job
    ldct_parms = {}

    # load JSON config file
    with open(f_job_cfg, 'r') as fhd:
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
    # ex: http://<host>:<port>/shared/clsim/201204110048BR6.tgz
    ls_link = "{}{}{:02d}{:02d}{}{:02d}{}.tgz".format(wdf.DS_FTP_URL,
                                                      ldct_parms["year"],
                                                      ldct_parms["month"],
                                                      ldct_parms["day"],
                                                      ldct_parms["hora"],
                                                      ldct_parms["delta"],
                                                      ldct_parms["regiao"])

    # exec WRF process
    try:
        # logger
        M_LOG.debug("subprocess.run: %s", str(["bash", str(wdf.DS_BASH_WRF), ls_parms]))

        # exec WRF
        subprocess.run(["bash", str(wdf.DS_BASH_WRF), ls_parms], capture_output=True, check=True)

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = ldct_parms["email"].strip()
        l_email["subject"] = "CLSim - Resultado da Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_OK.substitute(xtok=ls_parms,
                                                            xlink=ls_link))

        # send confirmation e-mail para o usuário
        wem.send_message(ldct_parms["email"].strip(), l_email.as_string())

        # remove token da fila
        pathlib.Path.unlink(f_job_cfg)

    # em caso de erro...
    except subprocess.CalledProcessError as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (WRF): %s", str(lerr.output.decode()))

        # obtem e compacta /home/webpca/WRF/WRF/test/em_real/rsl.error.0000
        # move para file server
        # gera o link

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = wdf.DS_EMAIL_WRF
        l_email["subject"] = "CLSim - Erro na Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_ERR.substitute(xtok=ls_parms,
                                                             xmsg=lerr.output.decode()))

        # enviar mail com aviso de erro para o meteorologista
        wem.send_message(wdf.DS_EMAIL_WRF, l_email.as_string())

        # rename job
        rename_job(f_job_cfg)

    # em caso de erro...
    except Exception as lerr:
        # logger
        M_LOG.error("execWRF abortou on subprocess.run (OS): %s", str(lerr))

        # create e-mail message
        l_email = email.message.EmailMessage()

        # build e-mail message
        l_email["from"] = wdf.DS_EMAIL_FROM
        l_email["to"] = wdf.DS_EMAIL_DEVL
        l_email["subject"] = "CLSim - Erro na Simulação"

        # build e-mail body
        l_email.set_content(wdf.DS_EMAIL_BODY_ERR.substitute(xtok=ls_parms,
                                                             xmsg=str(lerr)))

        # enviar mail com aviso de erro para o desenvolvedor
        wem.send_message(wdf.DS_EMAIL_DEVL, l_email.as_string())

        # rename job
        rename_job(f_job_cfg)

# ---------------------------------------------------------------------------------------------
def rename_job(f_job_cfg: pathlib.Path):
    """
    renomeia o arquivo de configuração do job
    """
    # logger
    M_LOG.debug("rename_job >>")

    # data atual (timestamp)
    li_now = int(time.time())

    # param filename
    ls_fname = pathlib.PurePath(wdf.DS_DIR_JOBS, f"{li_now}.json")

    # rename job
    f_job_cfg.rename(ls_fname)

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.info(">> main")

    # display
    print(" [*] Waiting for messages. To exit press CTRL+C")

    # forever...
    while True:
        # list of all files (json) in directory
        llst_files = glob.glob(os.path.join(wdf.DS_DIR_JOBS, "*.json"))
        # list of all files (json) in directory sorted by name
        llst_files = sorted(filter(os.path.isfile, llst_files))

        # tem jobs na fila ?
        if llst_files:
            # job file
            l_job_file = pathlib.Path(llst_files[0])

            # display
            print(" [x] Received ", str(l_job_file))

            # process job
            exec_job(l_job_file)

        # senão,...
        else:
            # allows task switch
            time.sleep(30)

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process
#
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
