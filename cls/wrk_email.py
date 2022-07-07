# -*- coding: utf-8 -*-
"""
wrk_email
send message to a list of users

2021.nov  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import email
import logging
import smtplib
import ssl

# local
import cls.cls_defs as df
import cls.wrf_defs as wdf

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def send_message(fs_to: str, fs_message: str):
    """
    send message to user

    :param fs_to (str): the mail's recipient
    :param fs_message (str): e-mail's body
    """
    # logger
    M_LOG.info(">> send_message")

    # create a secure SSL context
    l_context = ssl.create_default_context()

    # try to log in to server and send email
    try:
        # access server
        # l_server = smtplib.SMTP_SSL(host=wdf.DS_SMTP_SERVER, port=wdf.DI_SMTP_SSL_PORT)
        l_server = smtplib.SMTP(host=wdf.DS_SMTP_SERVER, port=wdf.DI_SMTP_PORT)
        assert l_server

        # logger
        M_LOG.debug("connection object: %s", str(l_server))

        # set debug level
        l_server.set_debuglevel(False)

        # server handshake
        # l_server.ehlo()  # can be omitted

        # secure the connection
        l_server.starttls(context=l_context)

        # server handshake
        # l_server.ehlo()  # can be omitted

    # em caso de erro,...
    except Exception as lerr:
        # logger
        M_LOG.error("error on email service: %s", lerr, exc_info=1)
        M_LOG.error("ref: %s", str(fs_message), exc_info=1)
        # cai fora
        return

    # logger
    M_LOG.debug("logging in.....")

    # try to log in to server and send email
    l_resp_code, l_response = l_server.login(wdf.DS_SMTP_USR, wdf.DS_SMTP_PWD)

    # logger
    M_LOG.debug("response code: %s", str(l_resp_code))
    M_LOG.debug("response: %s", str(l_response.decode()))

    # send message
    l_server.sendmail(wdf.DS_SMTP_USR, [fs_to], fs_message)
    
    M_LOG.debug("send to: %s", str([fs_to]))
    M_LOG.debug("sendmail: %s", str(fs_message))

    # logger
    M_LOG.debug("Logging Out....")

    # quit server
    l_resp_code, l_response = l_server.quit()

    # logger
    M_LOG.debug("response code: %s", str(l_resp_code))
    M_LOG.debug("response: %s", str(l_response.decode()))

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process
        
if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M",
                        format="%(asctime)s %(message)s",
                        level=logging.DEBUG)

    # create e-mail message
    l_email = email.message.EmailMessage()

    # build e-mail message
    l_email["from"] = wdf.DS_EMAIL_FROM
    l_email["to"] = wdf.DS_EMAIL_DEVL
    l_email["subject"] = "CLSim - Teste de e-mail"

    # build e-mail body
    l_email.set_content(wdf.DS_EMAIL_BODY_ERR.substitute(xtok="Teste",
                                                         xmsg="Mensagem teste"))
    print(l_email)

    # send message
    send_message("ml.abru@gmail.com", l_email.as_string())

# < the end >----------------------------------------------------------------------------------
