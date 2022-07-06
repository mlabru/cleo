# -*- coding: utf-8 -*-
"""
st_cli

2022.nov  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import json
import logging
import pathlib
import sys
import time

# local
import cls.cls_defs as df
import cls.wrf_defs as wdf

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def arg_parse():
    """
    parse command line arguments
    arguments parse: <initial date> <hour> <delta> <regiao> <email>

    :returns: string with parameters
    """
    # logger
    M_LOG.info(">> arg_parse")

    # número de parâmetros ok ?
    assert 6 == len(sys.argv), f"número de parâmetros ({len(sys.argv)}) inválido."

    # data início
    ldt_ini = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
    assert ldt_ini.date() >= datetime.date(2000, 1, 1), "data inicial < 2000-01-01"

    # hora início
    ls_hora_ini = str(sys.argv[2])
    assert ls_hora_ini in ["00", "06", "12", "18"], f"hora: {ls_hora_ini}"

    # intervalo de simulação
    li_dlt = int(sys.argv[3])
    assert li_dlt in [24, 48, 72], f"delta: {li_dlt}"

    # seleção da região
    ls_regiao = str(sys.argv[4])
    assert ls_regiao in wdf.DLST_REGIAO_SIGLA, f"região: {ls_regiao}"

    # e-mail
    ls_email = str(sys.argv[5])
    assert ls_email, "e-mail é obrigatório."

    # retorna parâmetros
    return {"year": ldt_ini.year, "month": ldt_ini.month, "day": ldt_ini.day,
            "hora": ls_hora_ini, "delta": li_dlt,
            "regiao": wdf.DLST_REGIAO_SIGLA[wdf.DLST_REGIAO_SIGLA.index(ls_regiao)],
            "email": ls_email}

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
    ls_fname = pathlib.PurePath(wdf.DS_DIR_JOBS, f"{li_now}.json")

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
    M_LOG.info(">> main")

    # get parameters
    ldct_parm = arg_parse()
    print(ldct_parm)

    # e-mail ok ?
    if ldct_parm["email"]:
        # submit button
        gera_job(ldct_parm)

        # logger
        print("O job foi enviado para execução.\n"
              "Um link para o resultado ou uma mensagem de erro "
              "retornará no e-mail selecionado em algumas horas.\n"
              "Obrigado.")

    # senão, e-mail inválido
    else:
        # error
        M_LOG.error("E-mail vazio ou inválido.")

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M",
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
