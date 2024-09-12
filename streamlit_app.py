# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import snowflake.connector
import requests
import pandas as pd

# Initialize connection.
conn = st.connection("snowflake")

base_url = "https://fruityvice.com/api/fruit/"



# Write directly to the app
st.title("Customize your Smoothie!")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smothie will be: ",name_on_order)


session = conn.session()
    
def get_fruit_data(fruit):
    response = requests.get(f"{base_url}{fruit}")
    if response.status_code == 200:
        return response
    else:
        return None
        
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data = my_dataframe, use_container_width=True)
st.stop()
ingredients_list = st.multiselect("Choose up to 5 ingredients:",my_dataframe, max_selections =5)
if ingredients_list:
    ingredients_string = ""
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + " "
        fruityvice_response = get_fruit_data(fruit_choosen) #requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        if fruityvice_response:
            st.subheader(fruit_choosen+ ' Nutrition Information')
            fv_df = st.dataframe(fruityvice_response.json(),use_container_width=True)
        else:
            st.write(f"Nutrition Information Not Available for {fruit_choosen}")

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



