import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError


streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Menu")

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toaast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
      
except URLError as e:
     streamlit.error()

def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

def insert_row_snowflake(fruit):
    with  my_cnx.cursor() as my_cur:
      my_cur.execute("Insert into fruit_load_list values('" +fruit +"')" )  
      return "thanks for adding "+ fruit
   
if streamlit.button('Get fruit load list'):
   
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input('What fruit would you like to  add?')
if streamlit.button('Add Fruit'):
   if(fruit_add.strip() != ""):
      streamlit.text(insert_row_snowflake(fruit_add));
   else:
     streamlit.error("Fruit is empty")
  
