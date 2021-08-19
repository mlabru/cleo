import streamlit as sl

sl.sidebar.title("Menu")
pg_sel = sl.sidebar.selectbox("Selecione o aplicativo", ["Cleo", "Ensemble"])

if "Cleo" == pg_sel:
    sl.title("Cleo")
    sl.selectbox("Região:", ["Norte", "Sul"])
    sl.date_input("Data:")

elif "Ensemble" == pg_sel:
    sl.title("Ensemble")
    x = sl.slider("x")
    sl.write(x, "squared is", x * x)
        
    
    

