import pydaisi as pyd
import streamlit as st

daisi2 = pyd.Daisi("laiglejm/Daisi2")

def fun3():
    res = daisi2.fun2().value

    return res

def st_ui():
    st.title("Tracebacks propagation example")

    st.write("Illustrate how tracebacks are propagated through a Daisi chain. This Daisi calls Daisi2 which itself calls Daisi1. Daisi1 produces an error which is propagated down to Daisi3")

    res = fun3()

if __name__ == "__main__":
    st_ui()