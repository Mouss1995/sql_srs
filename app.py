import streamlit as st
import pandas as pd
import duckdb
import io

csv = """
beverage, price
orange juice, 1.5
expresso, 2.5
tea, 3
"""

beverages = pd.read_csv(io.StringIO(csv))

csv2 = """
food_item, price
cookie, 3.5
chocolat, 2
muffin, 3
"""

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer).df()

st.header('Entrez votre requête :')

query = st.text_area(label="Votre code SQL ici", key='user_input')

if query :

   result = duckdb.sql(query).df()
   st.dataframe(result)


tab2, tab3 = st.tabs(['Tables', 'Solutions'])

with tab2:
   st.write("table: beverages")
   st.dataframe(beverages)
   st.write("table: food_items")
   st.dataframe(food_items)
   st.write("expected")
   st.dataframe(solution)

with tab3:
   st.write(answer)