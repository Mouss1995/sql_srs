"""Script for SQL-SRS application streamlit."""

import logging
import os
from datetime import date, timedelta, datetime

import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercices_sql_tables_duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that yser SQK query is correct by:
    1: Checking the columns
    2: checking the values
    :param user_query: a string containing SQL query
    """
    result = con.execute(user_query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        st.error("Some columns are missing")

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct")
            st.balloons()

    except KeyError as e:
        st.error("Some columns are missing")

    n_len_differences = result.shape[0] - solution_df.shape[0]

    if n_len_differences != 0:
        st.error(
            f"Result has a {n_len_differences} lines difference with the solution_df"
        )


theme_available = con.execute(
    "SELECT DISTINCT(theme) AS unique_theme FROM memory_state"
).df()
list_theme_available = theme_available["unique_theme"].tolist()

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        list_theme_available,
        index=None,
        placeholder="Select a theme ...",
    )

    if theme:
        st.write("You selected:", theme)

        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}' ORDER BY last_reviewed ASC"

    else:
        select_exercise_query = "SELECT * FROM memory_state ORDER BY last_reviewed ASC"

    exercise = con.execute(select_exercise_query).df().reset_index(drop=True)

    st.dataframe(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Entrez votre requête :")

query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)


for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset", type="primary"):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()  # Rerun in order to display the update dataframe

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
