# -*- coding: utf-8 -*-
"""
cleo

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import logging
import os

# graylog
import graypy

# pika (RabbitMQ client)
import pika

# streamlit
import streamlit as st

# .env
from dotenv import load_dotenv

# local
import cls_defs as dfs

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

# ---------------------------------------------------------------------------------------------
def pag_openwrf():
    """
    página de execução do OpenWRF
    """
    # logger
    M_LOG.debug("pag_openwrf >>")

    # top image
    st.image("wrfmodel.jpg")
    
    # título da página
    st.title("openWRF")

    # seleção da região
    ls_reg = st.selectbox("Região:", dfs.DLST_REGIAO_NOME)

    # cria 2 colunas
    lwd_col1, lwd_col2 = st.columns(2)

    # na coluna 1...
    with lwd_col1:
        # data início
        ldt_ini = st.date_input("Data Inicial (AAAA/MM/DD):")
        # intervalo de simulação
        li_dlt = st.selectbox("Intervalo de Simulação (horas):", [24, 48, 72])

    # na coluna 2...
    with lwd_col2:
        # hora início
        ls_hora_ini = st.selectbox("Hora Inicial:", ["00", "06", "12", "18"])

    # e-mail
    ls_email = st.text_input("E-mail para onde será enviado o arquivo de saída:")

    # gera parâmetros
    ls_parm = "{} {:04d} {:02d} {:02d} {} {:02d} {}".format(
              dfs.DLST_REGIAO_SIGLA[dfs.DLST_REGIAO_NOME.index(ls_reg)],
              ldt_ini.year, ldt_ini.month, ldt_ini.day, ls_hora_ini, li_dlt, 
              ls_email)

    # e-mail ok ?
    if not ls_email:
        # error
        st.error("E-mail vazio ou inválido.")

    # ok ?
    lv_ok = ls_email

    # submit button
    lv_submit = st.button("Gerar previsão", on_click=send_msg, args=(ls_parm,)) if lv_ok else False

    if lv_submit:
        # ok
        st.success("O job foi eviado para execução.\n" \
                   "Um link para o resultado retornará no e-mail selecionado em algumas horas.\n" \
                   "Obrigado.")

# ---------------------------------------------------------------------------------------------
def pag_frontline():
    """
    página de execução do Frontline
    """
    # logger
    M_LOG.debug("pag_frontline >>")

    # título da página
    st.title("Frontline (Carrapato Killer)")

    # cria 2 colunas
    lwd_col1, lwd_col2 = st.columns(2)

    # na coluna 1
    with lwd_col1:
        # data início
        ldt_ini = st.date_input("Data Inicial (AAAA/MM/DD):")
        # hora início
        ltm_ini = st.time_input("Hora Inicial (HH/MM):")

    # na coluna 2
    with lwd_col2:
        # data final
        ldt_fin = st.date_input("Data Final (AAAA/MM/DD):")
        # hora final
        ltm_fin = st.time_input("Hora Final (HH/MM):")

    x = st.slider("x")
    st.write(x, "squared is", x * x)

    # submit button
    lv_submit = st.button("Submit")
    
    if lv_submit:
        print("lv_submit:", lv_submit, type(lv_submit))
        print("ldt_ini:", ldt_ini, type(ldt_ini))
        print("ltm_ini:", ltm_ini, type(ltm_ini))
        print("ldt_fin:", ldt_fin, type(ldt_fin))
        print("ltm_fin:", ltm_fin, type(ltm_fin))

# ---------------------------------------------------------------------------------------------
def send_msg(fs_parm):
    """
    send message to queue 'execWRF'
    """
    # logger
    M_LOG.debug("send_msg >>")

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

    # create queue
    l_chnl.queue_declare(queue="execWRF", durable=True)

    # exec WRF
    l_chnl.basic_publish(exchange="",
                         routing_key="execWRF", 
                         body=fs_parm,
                         properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                        ))

    # logger
    M_LOG.info(" [x] Sent '{}'".format(fs_parm))

    # close connection
    l_conn.close()

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.info("main >>")

    # app title
    st.sidebar.title("Centro Logístico de Simulação Meteorológica")
    # app selection
    ls_pg_sel = st.sidebar.selectbox("Selecione o aplicativo", ["openWRF", "Frontline"])

    # openWRF ?
    if "openWRF" == ls_pg_sel:
        # call WRF page
        pag_openwrf()
        
    # frontline ?
    elif "Frontline" == ls_pg_sel:
        # call frontline page
        pag_frontline()
        
# ---------------------------------------------------------------------------------------------
# this is the bootstrap process
        
if "__main__" == __name__:
    # logger
    logging.basicConfig(level=dfs.DI_LOG_LEVEL)
 
    # disable logging
    # logging.disable(sys.maxint)

    # run application
    main()

# < the end >----------------------------------------------------------------------------------
