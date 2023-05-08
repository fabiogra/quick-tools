import base64

import streamlit as st

import style

st.set_page_config(
    page_title="Base64 Encoding and Decoding Converter - QuickTools",
    page_icon=":toolbox:",
    layout="wide",
)

st.markdown(style.clipboard_style, unsafe_allow_html=True)

st.title("Encode/Decode Any Text in Base64")

text = st.text_area("Enter your text here", key="text", height=200)
cols = st.columns(2)
output = st.empty()
with cols[0]:
    if st.button("Encode", use_container_width=True) and text != "":
        output.code(body=base64.b64encode(text.encode("utf-8")), language=None)
with cols[1]:
    if st.button("Decode", use_container_width=True) and text != "":
        try:
            output.code(body=base64.b64decode(text.encode("utf-8")), language=None)
        except ValueError:
            output.error("Invalid base64 string")
