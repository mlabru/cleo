import streamlit as st

st.sidebar.title("Centro Logístico de Simulação")
ls_pg_sel = st.sidebar.selectbox("Selecione o aplicativo", ["WRF", "Frontline"])

if "WRF" == ls_pg_sel:
    st.title("OpenWRF")
    ls_reg = st.selectbox("Região:", ["Norte", "Sudeste"])

    l_col1, l_col2 = st.columns(2)

    with l_col1:
        ls_dti = st.date_input("Data Inicial (AA/MM/DD):")
        ls_tmi = st.time_input("Hora Inicial (HH/MM):")

    with l_col2:
        ls_dtf = st.date_input("Data Final (AA/MM/DD):")
        ls_tmf = st.time_input("Hora Final (HH/MM):")

    l_ok = st.button("Submit")
    
    if l_ok:
        print("l_ok:", l_ok, type(l_ok))
        print("ls_reg:", ls_reg, type(ls_reg))
        print("ls_dti:", ls_dti, type(ls_dti))
        print("ls_tmi:", ls_tmi, type(ls_tmi))
        print("ls_dtf:", ls_dtf, type(ls_dtf))
        print("ls_tmf:", ls_tmf, type(ls_tmf))

elif "Frontline" == ls_pg_sel:
    st.title("Frontline (Carrapato Killer)")

    l_col1, l_col2 = st.columns(2)

    with l_col1:
        ls_dti = st.date_input("Data Inicial (AA/MM/DD):")
        ls_tmi = st.time_input("Hora Inicial (HH/MM):")

    with l_col2:
        ls_dtf = st.date_input("Data Final (AA/MM/DD):")
        ls_tmf = st.time_input("Hora Final (HH/MM):")

    x = st.slider("x")
    st.write(x, "squared is", x * x)

    l_ok = st.button("Submit")
    
    if l_ok:
        print("l_ok:", l_ok, type(l_ok))
        print("ls_dti:", ls_dti, type(ls_dti))
        print("ls_tmi:", ls_tmi, type(ls_tmi))
        print("ls_dtf:", ls_dtf, type(ls_dtf))
        print("ls_tmf:", ls_tmf, type(ls_tmf))
