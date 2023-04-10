import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Green Eggs and Ham')
streamlit.text('🥑🍞 Green Avocado and Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothies 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Banana','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice )
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) # How about some normalized json into a table?
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit for more information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

#streamlit.stop()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_WAREHOUSE()")

streamlit.header("The fruit_load_list contains:")
#snowflake-related functions

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("delete from fruit_load_list where fruit_name = '"+new_fruit+"'")
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return 'Thanks for adding ' + new_fruit
  
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

    
fruit_add = streamlit.text_input('What fruit would you like to add?')

if fruit_add:
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_row_snowflake(fruit_add)

# my_cnx.close()

