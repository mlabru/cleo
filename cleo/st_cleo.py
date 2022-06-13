# -*- coding: utf-8 -*-
"""
st_cleo

2022.jun  mlabru  remove rabbitmq cause of timeout problems, remove graylog
2022.may  mlabru  rabbitmq connection timeout
2022.apr  mlabru  graylog log management
2021.nov  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import json
import logging
import os
import pathlib
import sys
import time

# streamlit
import streamlit as st

# local
import cleo.cleo_defs as df
import cleo.wrf_defs as wdf

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

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
    ls_reg = st.selectbox("Região:", wdf.DLST_REGIAO_NOME)

    # cria 2 colunas
    lwd_col1, lwd_col2 = st.columns(2)

    # na coluna 1...
    with lwd_col1:
        # data início
        ldt_ini = st.date_input("Data Inicial (AAAA/MM/DD):",
                                min_value=datetime.date(2000, 1, 1))

        # intervalo de simulação
        li_dlt = st.selectbox("Intervalo de Simulação (horas):", [24, 48, 72])

    # na coluna 2...
    with lwd_col2:
        # hora início
        ls_hora_ini = st.selectbox("Hora Inicial:", ["00", "06", "12", "18"])

    # e-mail
    ls_email = st.text_input("E-mail para onde será enviado o link para o arquivo de saída:")

    # gera parâmetros
    ldct_parm = {"year": ldt_ini.year, "month": ldt_ini.month, "day": ldt_ini.day,
                 "hora": ls_hora_ini, "delta": li_dlt,
                 "regiao": wdf.DLST_REGIAO_SIGLA[wdf.DLST_REGIAO_NOME.index(ls_reg)],
                 "email": ls_email}

    # e-mail ok ?
    if ls_email:
        # submit button
        lv_submit = st.button("Gerar previsão",
                              on_click=gera_job,
                              args=(ldct_parm,))

        if lv_submit:
            # logger
            M_LOG.info(" [x] Sent '%s'", str(ldct_parm))

            # ok
            st.success("O job foi enviado para execução.\n"
                       "Um link para o resultado ou uma mensagem de erro "
                       "retornará no e-mail selecionado em algumas horas.\n"
                       "Obrigado.")

    # senão, e-mail inválido
    else:
        # error
        st.error("E-mail vazio ou inválido.")

# ---------------------------------------------------------------------------------------------
def gera_job(fdct_parm: dict):
    """
    gera o arquivo de configuração do job
    """
    # logger
    M_LOG.debug("gera_job >>")

    # data atual (timestamp)
    li_now = int(time.time())

    # param filename
    ls_fname = pathlib.PurePath(df.DS_DIR_JOBS, f"{li_now}.json")

    # open param file
    with open(ls_fname, 'w') as lfh_out:
        # write data directly from dictionary
        json.dump(fdct_parm, lfh_out)

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
    ls_pg_sel = st.sidebar.selectbox("Selecione o aplicativo", ["openWRF"])

    # openWRF ?
    if "openWRF" == ls_pg_sel:
        # call WRF page
        pag_openwrf()

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M",
                        format="%(asctime)s %(message)s",
                        level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxint)

    # run application
    main()

    # terminate
    sys.exit(0)

# < the end >----------------------------------------------------------------------------------
