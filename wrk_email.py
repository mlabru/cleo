# -*- coding: utf-8 -*-
"""
wrk_email
send message to user

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import email.mime.text as emt 
import logging
import os
import smtplib

# local
import cls_defs as df

# < defines >--------------------------------------------------------------------------------------

# SMTP host address
DS_SMTP_HOST = "smtp.mail.yahoo.com"
# SMTP normal port
DI_SMTP_PORT = 587
# SMTP SSL port
DI_SMTP_SSL_PORT = 465

# email from address
DS_EMAIL_FROM = "ml_sjc@yahoo.com.br"

# email from subject
DS_EMAIL_SUBJECT = "Resultado da Simulação"

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def send_email(flst_to, fs_link):
    """
    send email to user

    :param flst_to (str): the mail's array of recepients
    :param fs_link (str): mail's link to file
    """
    # e-mail recipients
    to_addrs = flst_to if isinstance(flst_to, list) else [flst_to]

    # create message
    lem_message = emt.MIMEText(fs_link)
    assert lem_message
    
    # message subject
    lem_message["subject"] = DS_EMAIL_SUBJECT
    # message sender
    lem_message["from"] = DS_EMAIL_FROM
    # message recipients
    lem_message["to"] = ", ".join(to_addrs)
    M_LOG.debug("lem_message: %s", lem_message)

    try:
        l_server = smtplib.SMTP(DS_SMTP_HOST, DI_SMTP_PORT)
        assert l_server
        
        l_server.starttls()
        l_server.login(df.hs.DS_YAH_USR, df.hs.DS_YAH_PWD)
        l_server.sendmail(DS_EMAIL_FROM, to_addrs, lem_message.as_string())
        l_server.quit()

        # logger
        M_LOG.info("successfully sent the mail.")
                
    # em caso de erro,...
    except:
        # logger
        M_LOG.error("Erro em email_service")

# < the end >--------------------------------------------------------------------------------------
