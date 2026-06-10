import pandas as pd 
import streamlit as st
import tempfile
import os

def save_uploaded_file(uploaded_file):
    """Save Streamlit uploaded file to a temp path and return the path."""
    suffix = os.path.splitext(uploaded_file.name)[-1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getvalue())
    tmp.flush()
    return tmp.name

@st.cache_data
def load_iris_csv():
    from sklearn.datasets import load_iris as _li
    iris = _li(as_frame=True)
    df   = iris.frame
    df.rename(columns={"target": "species"}, inplace=True)
    tmp  = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)
    return tmp.name, df