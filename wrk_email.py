# -*- coding: utf-8 -*-
"""
wrk_email
send message to user

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import email.mime.application as ema
import email.mime.multipart as emm 
import email.mime.text as emt 
import email.utils as eu

import logging
import os
import smtplib
import string

# local
import cls_defs as df

# < defines >--------------------------------------------------------------------------------------

# SMTP host address
DS_SMTP_HOST = "smtp.mail.yahoo.com"
# SMTP normal port
DI_SMTP_PORT = 587
# SMTP SSL port
DI_SMTP_SSL_PORT = 465

# email template
DS_EMAIL_ATTACH = "Segue o resultado da simulação."
# email template
DS_EMAIL_BODY = string.Template("Segue o link com o resultado da simulação:\n\n$link.")
# email from subject
DS_EMAIL_SUBJECT = "Resultado da Simulação"

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def _send_message(flst_to, fem_message):
    """
    send message to user

    :param flst_to (list): the mail's array of recipients
    :param fem_message (MIMEMultipart): e-mail's body
    """
    try:
        # connect server
        l_server = smtplib.SMTP(DS_SMTP_HOST, DI_SMTP_PORT)
        assert l_server
        
        # server handshake
        l_server.starttls()
        l_server.login(df.hs.DS_YAH_USR, df.hs.DS_YAH_PWD)
        l_server.sendmail(df.hs.DS_YAH_USR, flst_to, fem_message.as_string())
        l_server.quit()

        # logger
        M_LOG.info("Successfully sent the mail.")
                
    # em caso de erro,...
    except:
        # logger
        M_LOG.error("Erro em email_service")

# -------------------------------------------------------------------------------------------------
def send_email(flst_to, fs_token, fv_upload=df.DV_RESULT_UPLOAD):
    """
    send confirmation e-mail

    :param flst_to (str): recipients
    :param fs_token (str): document_me
    :param fv_upload (bool): document_me
    """
    # e-mail recipients
    llst_to = flst_to if isinstance(flst_to, list) else [flst_to]

    # create e-mail
    lem_message = emm.MIMEMultipart()
    assert lem_message

    # message subject
    lem_message["subject"] = DS_EMAIL_SUBJECT
    # message sender
    lem_message["from"] = df.hs.DS_YAH_USR
    # message recipients
    lem_message["to"] = eu.COMMASPACE.join(llst_to)
    # message date
    lem_message["date"] = eu.formatdate(localtime=True)
    M_LOG.debug("lem_message: %s", lem_message)

    # upload file ?
    if fv_upload:
        # upload file to Google Drive
        ls_link = wul.upload_file(fs_token)
        M_LOG.debug("ls_link: %s", ls_link)

        if ls_link:
            # e-mail link to user
            lem_message.attach(emt.MIMEText(DS_EMAIL_BODY.substitute(link=ls_link)))

    # attach ?
    if not fv_upload:
        # e-mail link to user
        lem_message.attach(emt.MIMEText(DS_EMAIL_ATTACH))

        file_send = fs_token
        
        # for all files to attach...
        with open(file_send, "rb") as lfh:
            # create MIME application
            lma_part = ema.MIMEApplication(lfh.read(), Name=os.path.basename(file_send))
            assert lma_part
            
            # after the file is closed
            lma_part["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(file_send)

            # attach to body
            lem_message.attach(lma_part)

    # send message
    _send_message(llst_to, lem_message)
                
# < the end >--------------------------------------------------------------------------------------
