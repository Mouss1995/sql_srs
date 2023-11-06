"""Script for SQL-SRS application streamlit."""

import io
import ast
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
        ["cross_joins", "GroupBy", "window_functions"],
        index=None,
        placeholder="Select a theme ...",
    )

    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Entrez votre requête :")

query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        st.error("Some columns are missing")

    try:
        result = result[solution_df.columns]

    except KeyError as e:
        st.error("Some columns are missing")

    n_len_differences = result.shape[0] - solution_df.shape[0]

    if n_len_differences != 0:
        st.error(
            f"Result has a {n_len_differences} lines difference with the solution_df"
        )

tab2, tab3 = st.tabs(["Tables", "Solution"])


with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f'SELECT * FROM {table}').df()
        st.dataframe(df_table)
        
with tab3:

    st.write(answer)
