# -*- coding: utf-8 -*-
"""
cleo_pika

2022.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os

# dotenv
import dotenv

# graylog
import graypy

# pika (RabbitMQ client)
import pika

# local
import cleo.cleo_defs as df

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# message queue user/passwd
DS_MSQ_USR = os.getenv("DS_MSQ_USR")
DS_MSQ_PWD = os.getenv("DS_MSQ_PWD")

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# graylog handler
M_GLH = graypy.GELFUDPHandler("localhost", 12201)
M_LOG.addHandler(M_GLH)

# pika logger
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.ERROR)

# ---------------------------------------------------------------------------------------------
def create_channel():
    """
    send message to queue 'DS_MSQ_QUEUE'
    """
    # logger
    M_LOG.info(">> create_channel")

    # create credentials
    l_cred = pika.PlainCredentials(DS_MSQ_USR, DS_MSQ_PWD)
    assert l_cred

    # create parameters
    l_parm = pika.ConnectionParameters(host=df.DS_MSQ_SRV, credentials=l_cred)
    assert l_parm

    # RabbitMQ connection exceptions
    lset_connect_exceptions = (pika.exceptions.ConnectionClosed,
                               pika.exceptions.AMQPConnectionError,
                               pika.exceptions.IncompatibleProtocolError)

    try:
        # create connection
        l_conn = pika.BlockingConnection(l_parm)
        assert l_conn

    # em caso de erro...
    except lset_connect_exceptions as l_err:
        # logger
        M_LOG.debug("DS_MSQ_USR: %s", DS_MSQ_USR)
        M_LOG.debug("DS_MSQ_PWD: %s", DS_MSQ_PWD)
        M_LOG.debug("DS_MSQ_SRV: %s", df.DS_MSQ_SRV)

        # logger
        M_LOG.error("RabbitMQ error: %s, reconnect.", str(l_err))

    # em caso de erro...
    except AttributeError as l_err:
        # logger
        M_LOG.debug("DS_MSQ_USR: %s", DS_MSQ_USR)
        M_LOG.debug("DS_MSQ_PWD: %s", DS_MSQ_PWD)
        M_LOG.debug("DS_MSQ_SRV: %s", df.DS_MSQ_SRV)

        # logger
        M_LOG.error("RabbitMQ error: %s, reconnect.", str(l_err))

    # create channel
    l_chnl = l_conn.channel()
    assert l_chnl

    # create execWRF queue
    l_chnl.queue_declare(queue=df.DS_MSQ_QUEUE, durable=True)

    # return
    return l_conn, l_chnl

# < the end >----------------------------------------------------------------------------------
