# -*- coding: utf-8 -*-
"""
worker
work queue consumer

2022/apr  1.1  mlabru  graylog log management
2021/nov  1.0  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os
import pathlib
import subprocess
import sys

# graylog
import graypy

# pika
import pika

# dotenv
from dotenv import load_dotenv

# local
import cls_defs as dfs
import wrk_email as wem

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
load_dotenv()

# message queue user/passwd
DS_MSQ_USR = os.getenv("DS_MSQ_USR")
DS_MSQ_PWD = os.getenv("DS_MSQ_PWD")

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(dfs.DI_LOG_LEVEL)

# graylog handler
M_GLH = graypy.GELFUDPHandler("localhost", 12201)
M_LOG.addHandler(M_GLH)

# pika logger
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.ERROR)

# < defines >----------------------------------------------------------------------------------

# source path
DS_SRC_PATH = pathlib.Path(__file__).resolve().parent

# execWRF batch
DS_BASH_WRF = pathlib.PurePath(DS_SRC_PATH, "execWRF.sh")

# ---------------------------------------------------------------------------------------------
def callback(f_ch, f_method, f_properties, f_body):
    """
    process messages callback

    :param f_ch: document_me
    :param f_method: document_me
    :param f_properties: document_me
    :param f_body: document_me
    """
    # logger
    M_LOG.debug("callback >>")

    # get parameters
    ls_parms = f_body.decode()

    # logger
    M_LOG.info(" [x] Received %r" % ls_parms)

    # strip parameters
    llst_parms = ls_parms.split()

    # token
    ls_token = "".join(llst_parms[:-1])

    # exec WRF
    ls_log = subprocess.run(["bash", DS_BASH_WRF, ls_parms], capture_output=True)

    # send confirmation e-mail
    # wem.send_email(llst_parms[-1].strip(), ls_token, False)

    # message acknowledgment
    f_ch.basic_ack(delivery_tag=f_method.delivery_tag)

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.debug("main >>")

    # create credentials
    l_cred = pika.PlainCredentials(DS_MSQ_USR, DS_MSQ_PWD)
    assert l_cred

    # create parameters
    l_parm = pika.ConnectionParameters(host=dfs.DS_MSQ_SRV, credentials=l_cred)
    assert l_parm
    
    # create connection
    l_conn = pika.BlockingConnection(l_parm)
    assert l_conn

    # create channel
    l_chnl = l_conn.channel()
    assert l_chnl

    # create execWRF queue
    l_chnl.queue_declare(queue="execWRF", durable=True)

    # dispatch to the next worker that is not still busy
    l_chnl.basic_qos(prefetch_count=1)

    # create consume
    l_chnl.basic_consume(queue="execWRF", on_message_callback=callback)  # , auto_ack=True)

    # logger
    M_LOG.info(" [*] Waiting for messages. To exit press CTRL+C")

    # start consuming
    l_chnl.start_consuming()

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%d/%m/%Y %H:%M",
                        format="%(asctime)s %(message)s",
                        level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxint)

    try:
        # run application
        main()

    # em caso de erro...
    except KeyboardInterrupt:
        # logger
        logging.warning("Interrupted.")

        try:
            # terminate
            sys.exit(0)

        # em caso de erro...
        except SystemExit:
            # quit
            os._exit(0)

# < the end >----------------------------------------------------------------------------------
            