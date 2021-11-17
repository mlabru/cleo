# -*- coding: utf-8 -*-
"""
cleo

2021/nov  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import datetime
import logging

# pika (RabbitMQ client)
import pika

# streamlit
import streamlit as st

# local
import cls_defs as df

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < defines >--------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
def pag_openwrf():
    """
    página de execução do OpenWRF
    """
    # top image
    st.image("wrfmodel.jpg")
    
    # título da página
    st.title("openWRF")

    # seleção da região
    ls_reg = st.selectbox("Região:", df.DLST_REGIAO_NOME)

    # cria 2 colunas
    lwd_col1, lwd_col2 = st.columns(2)

    # na coluna 1
    with lwd_col1:
        # data início
        ldt_ini = st.date_input("Data Inicial (AAAA/MM/DD):")
        # hora início
        ltm_ini = st.time_input("Hora Inicial (HH/MM):")
        # data & hora
        ldt_ini = datetime.datetime(ldt_ini.year, ldt_ini.month, ldt_ini.day, ltm_ini.hour, ltm_ini.minute, 0)

    # na coluna 2
    with lwd_col2:
        # data final
        ldt_fin = st.date_input("Data Final (AAAA/MM/DD):")
        # hora final
        ltm_fin = st.time_input("Hora Final (HH/MM):")
        # data & hora
        ldt_fin = datetime.datetime(ldt_fin.year, ldt_fin.month, ldt_fin.day, ltm_fin.hour, ltm_fin.minute, 0)

    # calculate delta time
    ldt_dlt = ldt_fin - ldt_ini
    # em segundos
    lf_dlt_in_s = ldt_dlt.total_seconds() 
    # em horas
    lf_dlt_in_h = divmod(lf_dlt_in_s, 3600)[0]

    # e-mail
    ls_email = st.text_input("E-mail para onde serão enviados os arquivos de saída:")

    # gera parâmetros
    ls_parm = "{} {} {} {} {} {} {} {} {} {} {} {}".format(
                  df.DLST_REGIAO_SIGLA[df.DLST_REGIAO_NOME.index(ls_reg)],
                  ldt_ini.year, ldt_ini.month, ldt_ini.day, ldt_ini.hour, ldt_ini.minute,
                  ldt_fin.year, ldt_fin.month, ldt_fin.day, ldt_fin.hour, ldt_fin.minute,
                  ls_email)

    # senão, data ok ?
    if ldt_ini >= ldt_fin:
        # error
        st.error("Data final deve ser posterior a inicial.")

    # senão, delta ok ?
    elif lf_dlt_in_h > df.DI_DELTA:    
        # error
        st.error("Intervalo de previsão maior que {} horas.".format(df.DI_DELTA))

    # e-mail ok ?
    elif not ls_email:
        # error
        st.error("E-mail vazio ou inválido.")

    # ok ?
    lv_ok = ls_email and (ldt_fin > ldt_ini) and (lf_dlt_in_h <= df.DI_DELTA)

    # submit button
    lv_submit = st.button("Gerar previsão", on_click=send_msg, args=(ls_parm,)) if lv_ok else False

    if lv_submit:
        # send message
        send_msg(ls_parm)
        # ok
        st.success("O job foi eviado para execução. O resultado retornará no e-mail selecionado em algumas horas. Obrigado.")

# -------------------------------------------------------------------------------------------------
def pag_frontline():
    """
    página de execução do Frontline
    """
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

# -------------------------------------------------------------------------------------------------
def send_msg(fs_parm):
    """
    send message to queue 'execWRF'
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

    # create queue
    l_chnl.queue_declare(queue="execWRF")

    # exec WRF
    l_chnl.basic_publish(exchange="", routing_key="execWRF", body=fs_parm)

    # logger
    M_LOG.info(" [x] Sent '{}'".format(fs_parm))

    # close connection
    l_conn.close()

# -------------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
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
        
# -------------------------------------------------------------------------------------------------
# this is the bootstrap process
        
if "__main__" == __name__:
    # logger
    logging.basicConfig(level=logging.DEBUG)
 
    # disable logging
    # logging.disable(sys.maxint)

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
