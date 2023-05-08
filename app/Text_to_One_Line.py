import streamlit as st

import style

st.set_page_config(
    page_title="Text to One Line Converter - QuickTools",
    page_icon=":toolbox:",
    layout="wide",
)

st.markdown(style.clipboard_style, unsafe_allow_html=True)

st.title("Convert Any Text to a One Line")

text = st.text_area("Enter your text here", key="text", height=200)
output = st.empty()

if text != "":
    st.code(body=text.replace("\n", " "), language=None)
    st.caption("Lenght: " + str(len(text)) + " characters")
