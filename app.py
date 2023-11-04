"""Script for SQL-SRS application streamlit."""

import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage, price
orange juice, 1.5
expresso, 2.5
tea, 3
"""

beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item, price
cookie, 3.5
chocolat, 2
muffin, 3
"""

food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ["Joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme ...",
    )

    st.write("You selected:", option)

st.header("Entrez votre requête :")

query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        st.error("Some columns are missing")

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))

    except KeyError as e:
        st.error("Some columns are missing")

    n_len_differences = result.shape[0] - solution_df.shape[0]

    if n_len_differences != 0:
        st.error(
            f"Result has a {n_len_differences} lines difference with the solution_df"
        )

tab2, tab3 = st.tabs(["Tables", "solution_dfs"])


with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
