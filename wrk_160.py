# -*- coding: utf-8 -*-
"""
msq_160
160 work queue consumer

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import pathlib
import subprocess
import sys

# pika
import pika

# local
import cls_defs as df

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < defines >--------------------------------------------------------------------------------------

# source path
DS_SRC_PATH = pathlib.Path(__file__).resolve().parent

# execWRF batch
DS_BASH_WRF = pathlib.PurePath(DS_SRC_PATH, "execWRF.sh")

# -------------------------------------------------------------------------------------------------
def callback(f_ch, f_method, f_properties, f_body):
    """
    process messages callback

    :param f_ch: document_me
    :param f_method: document_me
    :param f_properties: document_me
    :param f_body: document_me
    """
    # logger
    M_LOG.info(" [x] Received %r" % f_body.decode())

    # exec WRF
    ls_log = subprocess.run(["bash", DS_BASH_WRF, f_body.decode()], capture_output=True)
    M_LOG.debug("ls_log: %s", ls_log)

    # message acknowledgment
    f_ch.basic_ack(delivery_tag=f_method.delivery_tag)
        
# -------------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # create credentials
    l_cred = pika.PlainCredentials(df.DS_USER, df.DS_PASS)
    assert l_cred

    # create parameters
    l_parm = pika.ConnectionParameters(host=df.DS_MSGQ_SRV, credentials=l_cred)
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

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(level=logging.DEBUG)

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

# < the end >--------------------------------------------------------------------------------------
            