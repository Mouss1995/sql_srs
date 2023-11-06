"""Script for SQL-SRS application streamlit."""

import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect(database='data/exercices_sql_tables.duckdb', read_only=False)

# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """

# solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ["cross_joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme ...",
    )

    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Entrez votre requête :")

query = st.text_area(label="Votre code SQL ici", key="user_input")

# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)

#     if len(result.columns) != len(solution_df.columns):
#         st.error("Some columns are missing")

#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))

#     except KeyError as e:
#         st.error("Some columns are missing")

#     n_len_differences = result.shape[0] - solution_df.shape[0]

#     if n_len_differences != 0:
#         st.error(
#             f"Result has a {n_len_differences} lines difference with the solution_df"
#         )

# tab2, tab3 = st.tabs(["Tables", "solution_dfs"])


# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected")
#     st.dataframe(solution_df)

# with tab3:
#     st.write(ANSWER_STR)
