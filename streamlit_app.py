# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import snowflake.connector
import requests
import pandas as pd

# Initialize connection.
conn = st.connection("snowflake")





# Write directly to the app
st.title("Customize your Smoothie!")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smothie will be: ",name_on_order)


session = conn.session()
    

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data = my_dataframe, use_container_width=True)
ingredients_list = st.multiselect("Choose up to 5 ingredients:",my_dataframe, max_selections =5)
if ingredients_list:
    ingredients_string = ""
    
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    #fv_df_pandas = pd.DataFrame(fruityvice_response.json())
    #fv_df_pandas = fv_df_pandas[fv_df_pandas['name'].isin(ingredients_list)]
    fv_df = st.dataframe(fruityvice_response.json(),use_container_width=True)

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + " "

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """',
            '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")



