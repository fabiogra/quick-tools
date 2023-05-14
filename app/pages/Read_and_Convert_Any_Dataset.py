import io
import streamlit as st
import pandas as pd
import os
import style


SUPPORTED_FORMATS_AND_READ_METHODS = {
    "csv": (pd.read_csv, {"sep": ","}),
    "tsv": (pd.read_csv, {"sep": "\t"}),
    "json": (pd.read_json, {}),
    "xls": (pd.read_excel, {"engine": "openpyxl"}),
    "xlsx": (pd.read_excel, {"engine": "openpyxl"}),
    "html": (pd.read_html, {}),
    "hdf5": (pd.read_hdf, {}),
    "parquet": (pd.read_parquet, {}),
    "feather": (pd.read_feather, {}),
    "xml": (pd.read_xml, {}),
    "yaml": (pd.read_xml, {}),
}
SUPPORTED_FORMATS_AND_WRITE_METHODS = {
    "csv": ("to_csv", {"sep": ",", "index": False}),
    "tsv": ("to_csv", {"sep": "\t", "index": False}),
    "json": ("to_json", {}),
    "xls": ("to_excel", {"engine": "openpyxl", "index": False}),
    "xlsx": ("to_excel", {"engine": "openpyxl", "index": False}),
    "parquet": ("to_parquet", {}),
    "feather": ("to_feather", {}),
    "xml": ("to_xml", {"index": False}),
}

list_of_formats_str = ", ".join(SUPPORTED_FORMATS_AND_READ_METHODS.keys())

st.set_page_config(
    page_title=f"Convert Any Dataset ({list_of_formats_str}) - QuickTools",
    page_icon=":toolbox:",
    layout="wide",
)

st.markdown(style.clipboard_style, unsafe_allow_html=True)

st.title("Read and Convert Any Dataset")
st.subheader("Supported formats: " + list_of_formats_str)


def read_dataset(input_file: str, extension=None):
    if extension is None:
        name, ext = os.path.splitext(input_file.name)
        extension = ext.lstrip(".").lower()

    pd_read_func_and_kwargs = SUPPORTED_FORMATS_AND_READ_METHODS.get(extension, None)
    if pd_read_func_and_kwargs is not None:
        pd_read_func, pd_read_kwargs = pd_read_func_and_kwargs
        return name, pd_read_func(input_file, **pd_read_kwargs)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


@st.cache_data
def write_dataset(df: pd.DataFrame, output_file: str, extension: str):
    pd_write_func_and_kwargs = SUPPORTED_FORMATS_AND_WRITE_METHODS.get(extension, None)
    if pd_write_func_and_kwargs is not None:
        pd_write_func, pd_write_kwargs = pd_write_func_and_kwargs
        pd_write_func = eval(f"df.{pd_write_func}")
        _buffer = io.BytesIO()
        pd_write_func(_buffer, **pd_write_kwargs)
        return _buffer
    else:
        raise ValueError(f"Unsupported file format: {extension}")


input_file = st.file_uploader(
    "Upload your dataset", type=SUPPORTED_FORMATS_AND_READ_METHODS.keys()
)

if input_file is not None:
    name, df = read_dataset(input_file)
    st.dataframe(data=df, use_container_width=True)

    # Let the user choose the output format
    output_format = st.selectbox(
        "Choose the output format",
        ["..."] + list(SUPPORTED_FORMATS_AND_WRITE_METHODS.keys()),
    )
    if output_format != "...":
        st.download_button(
            label="Download data as " + output_format.upper(),
            data=write_dataset(df, name, output_format),
            file_name=f"{name}.{output_format}",
            use_container_width=True,
        )
