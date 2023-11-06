# pylint: disable=missing-module-docsting

import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect("data/exercices_sql_tables.duckdb", read_only=False)


# --------------------------------------------------
# CROSS JOINS EXERCICES
# --------------------------------------------------

data = {
    "theme": ["cross_joins", "window_functions"],
    "exercise_name": ["beverages_and_food", "simple_window"],
    "tables": [["beverages", "food_items"], "simple_windows"],
    "last_reviewed": ["1970-01-01", "1970-01-01"],
}

memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# --------------------------------------------------
# CROSS JOINS EXERCICES
# --------------------------------------------------

CSV = """
beverage, price
orange juice, 1.5
expresso, 2.5
tea, 3
"""

beverages = pd.read_csv(io.StringIO(CSV))

con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item, price
cookie, 3.5
chocolat, 2
muffin, 3
"""

food_items = pd.read_csv(io.StringIO(CSV2))

con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")
