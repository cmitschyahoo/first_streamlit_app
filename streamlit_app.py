import streamlit
import pandas

streamlit.title('New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Green Eggs and Ham')
streamlit.text('🥑🍞 Green Avocado and Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
