# Import python packages
import streamlit as st
from snowflake.snowpark.context  import get_active_session
from snowflake.snowpark.functions import col # snowpark


# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie.
    """
)
cnx = st.connection("snowflake")
session = cnx.session()
## creation of the text input box

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be: ',name_on_order);


# Creation of a select box
#option = st.selectbox(
    #'What is your favorite fruit?',('Banana', 'Strawberries','Peaches')
#)

#st.write ('You selected: ', option)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe (data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect( #cool multi select
    'Choose up to 5 ingredients: '
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredient_string = ''

    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '

    st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!',icon="🍌")
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
