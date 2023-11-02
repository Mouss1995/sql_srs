import streamlit as st
import pandas as pd
import duckdb
import io

option = st.selectbox(
    "What would you like to review ?",
    ['Joins', 'GroupBy', 'Windows Functions'],
    index=None,
    palceholder='Select a theme ...'
)

st.write('You selected:', option)

data = {'a': [1, 2, 3], 'b':[4, 5, 6]}

df = pd.DataFrame(data)