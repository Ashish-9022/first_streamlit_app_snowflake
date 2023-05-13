import streamlit as st
import pandas as pd
import requests as req
import snowflake.connector
from urllib.error import URLError

st.title("My first sstreamlit app")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
st.text('Omega 3 & Blueberry Oatmeal')
st.text('Kale, Spinach & Rocket Smoothie')
st.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

f_res = req.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
fruityvice_normalized = pd.json_normalize(f_res.json())


st.dataframe(fruityvice_normalized)

try:
  add_fruit = st.text_input('What fruit would you add?')
  if not add_fruit:
    st.error('Please inter fruit name')
  else:
    f_res = req.get(f'https://fruityvice.com/api/fruit/{add_fruit}')
    fruityvice_normalized = pd.json_normalize(f_res.json())
    st.dataframe(fruityvice_normalized)
except URLError as err:
  st.error(err)
    



my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
st.text("Hello from Snowflake:")
st.dataframe(my_data_row)
#st.text(fruityvice_normalized)

if not add_fruit:
  add_f_exr= my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values('{add_fruit}')")
  adf_f_exe_res = my_cur.fetchall()
  st.text(adf_f_exe_res)
  if adf_f_exe_res[0][0]==1:
    st.write('Inserted - ', add_fruit)

