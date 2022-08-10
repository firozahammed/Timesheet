import base64
from datetime import datetime
import datetime as dt
from datetime import date

import pyodbc
import streamlit as st
from PIL import Image

# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("Timesheet")
sheet = workbook.sheet1

sheet_url = st.secrets["private_gsheets_url"]
# this function is called when saving response of a customer visit
def insert_client(mysum, client_name_1, loc1, country1, mysum2, client_name_2, loc2, country2, mysum3, client_name_3,
                  loc3, country3):
    array[5] = mysum
    array[6] = client_name_1
    array[7] = country1
    array[8] = loc1
    array[9] = mysum2
    array[10] = client_name_2
    array[11] = country2
    array[12] = loc2
    array[13] = mysum3
    array[14] = client_name_3
    array[15] = country3
    array[16] = loc3


# this function is called when saving vendor visits
def insert_vendor(mysum, vendor_name_1, mysum2, vendor_name_2):
    array[19] = mysum
    array[20] = vendor_name_1
    array[21] = mysum2
    array[22] = vendor_name_2


# this function saves business trips responses
def insert_business_trip(country, location, date_from, date_to):
    array[23] = country
    array[24] = location
    array[25] = date_from
    array[26] = date_to


# this function is called to initialize the responses array and @st.cache insures its called only once
@st.experimental_singleton()
def initialize_array():
    array = ['-'] * 29
    array[0] = ""
    array[1] = ""
    array[2] = str(date.today())
    return array

@st.cache(allow_output_mutation=True)
def reinitialize_array(array):
    new_array = ['-'] * 29
    new_array[0] = ""
    new_array[1] = ""
    new_array[2] = str(date.today())
    return array


# this function is used to calculate the time submitted in the form
def calculate_time(start_time1, end_time1):
    mysum = dt.timedelta()
    (h, m, s) = start_time1.split(':')
    (h2, m2, s2) = end_time1.split(':')
    d = dt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    d2 = dt.timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2))
    mysum = d2 - d
    return mysum


# setting the form background
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


#set_bg_hack('background.png')

image = Image.open("OIP.jpg")
st.image(image)
array=initialize_array()
# a flag to be used later for finishing execution
finish = False

# setting up the form page
st.title('specify all late reasons below')
options = (
    '----', 'Customer visit', 'Hospital visit', 'Vendor visit', 'Business trip', 'Personal excuse', 'Reporting late')
selection = st.selectbox("Dear NA u have been late for today's attendance for '00:00', please choose a reason",
                         options)

# these if statements are for setting up the form selection box
if selection == 'Customer visit':
    clm1, clm2, clm3, clm4, clm5 = st.columns(5)
    client_name_1 = clm1.text_input('Client name 1')
    client_name_2 = clm1.text_input('Client name 2')
    client_name_3 = clm1.text_input('Client name 3')
    loc1 = clm3.text_input('location:', key=1)
    loc2 = clm3.text_input('location:', key=2)
    loc3 = clm3.text_input('location:', key=3)
    country1 = clm2.text_input('country:', key=1)
    country2 = clm2.text_input('country:', key=2)
    country3 = clm2.text_input('country:', key=3)
    # these if statements just to make the time slots appear after typing in a name for clearnce
    if client_name_1:
        start_time1 = str(clm4.time_input('from:', datetime.now(), 1))
        end_time1 = str(clm5.time_input('to:', datetime.now(), 1))
    if client_name_2:
        start_time_2 = str(clm4.time_input('from:', datetime.now(), 2))
        end_time_2 = str(clm5.time_input('to:', datetime.now(), 2))
    if client_name_3:
        start_time_3 = str(clm4.time_input('from:', datetime.now(), 3))
        end_time_3 = str(clm5.time_input('to:', datetime.now(), 3))
    save_add_button = clm4.button('save/add')
    if save_add_button:
        # handling of time exceptions
        try:
            mysum = str(calculate_time(start_time1, end_time1))
        except:
            mysum = '00:00:00'
        try:
            mysum2 = str(calculate_time(start_time_2, end_time_2))
        except:
            mysum2 = '00:00:00'
        try:
            mysum3 = str(calculate_time(start_time_3, end_time_3))
        except:
            mysum3 = '00:00:00'
        # calling insertion function
        insert_client(mysum, client_name_1, loc1, country1, mysum2, client_name_2, loc2, country2, mysum3,
                      client_name_3, loc3, country3)
        st.success('response added')
    save_exit_button = clm5.button('save/exit')
    if save_exit_button:
        # handling time exceptions
        try:
            mysum = str(calculate_time(start_time1, end_time1))
        except:
            mysum = '00:00:00'
        try:
            mysum2 = str(calculate_time(start_time_2, end_time_2))
        except:
            mysum2 = '00:00:00'
        try:
            mysum3 = str(calculate_time(start_time_3, end_time_3))
        except:
            mysum3 = '00:00:00'
        # calling insertion method
        insert_client(mysum, client_name_1, loc1, country1, mysum2, client_name_2, loc2, country2, mysum3,
                      client_name_3, loc3, country3)
        # this will make the form print the saved results and stop the execution
        finish = True

elif selection == 'Hospital visit':
    clm1, clm2, clm3 = st.columns(3)
    location = clm1.text_input('location')
    start_time1 = str(clm2.time_input('from:', datetime.now(), 1))
    end_time1 = str(clm3.time_input('to:', datetime.now(), 1))
    save_add_button = clm2.button('save/add')
    if save_add_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[17] = mysum
        array[18] = location
        st.success('response added')
    save_exit_button = clm3.button('save/exit')
    if save_exit_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[17] = mysum
        array[18] = location
        finish = True

elif selection == 'Vendor visit':
    clm1, clm2, clm3 = st.columns(3)
    vendor_name_1 = clm1.text_input('vendor name 1')
    vendor_name_2 = clm1.text_input('vendor name 2')
    # this to make time slots appear after inputting a name
    if vendor_name_1:
        start_time1 = str(clm2.time_input('from:', datetime.now(), 1))
        end_time1 = str(clm3.time_input('to:', datetime.now(), 1))
    if vendor_name_2:
        start_time_2 = str(clm2.time_input('from:', datetime.now(), 2))
        end_time_2 = str(clm3.time_input('to:', datetime.now(), 2))
    save_add_button = clm2.button('save/add')
    if save_add_button:
        # handling time exceptions
        try:
            mysum = str(calculate_time(start_time1, end_time1))
        except:
            mysum = '00:00:00'
        try:
            mysum2 = str(calculate_time(start_time_2, end_time_2))
        except:
            mysum2 = '00:00:00'
        # calling insertion function
        insert_vendor(mysum, vendor_name_1, mysum2, vendor_name_2)
        st.success('response added')
    save_exit_button = clm3.button('save/exit')
    if save_exit_button:
        # handling time exception
        try:
            mysum = str(calculate_time(start_time1, end_time1))
        except:
            mysum = '00:00:00'
        try:
            mysum2 = str(calculate_time(start_time_2, end_time_2))
        except:
            mysum2 = '00:00:00'
        # calling insertion function
        insert_vendor(mysum, vendor_name_1, mysum2, vendor_name_2)
        finish = True

elif selection == 'Business trip':
    clm1, clm2, clm3, clm4 = st.columns(4)
    country = clm1.text_input('country:')
    location = clm2.text_input('location:')
    if country:
        date_from = str(clm3.date_input('from'))
        date_to = str(clm4.date_input('to'))
    save_add_button = clm3.button('save/add')
    if save_add_button:
        # calling insertion function
        try:
            insert_business_trip(country, location, date_from, date_to)
        except:
            insert_business_trip(country, location, '', '')
        st.success('response added')
    save_exit_button = clm4.button('save/exit')
    if save_exit_button:
        # calling insertion function
        try:
            insert_business_trip(country, location, date_from, date_to)
        except:
            insert_business_trip(country, location, '', '')
        finish = True

elif selection == 'Personal excuse':
    clm1, clm2, clm3 = st.columns(3)
    start_time1 = str(clm2.time_input('from:', datetime.now(), 1))
    end_time1 = str(clm3.time_input('to:', datetime.now(), 1))
    save_add_button = clm2.button('save/add')
    if save_add_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[27] = mysum
        st.success('response added')
    save_exit_button = clm3.button('save/exit')
    if save_exit_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[27] = mysum
        finish = True

elif selection == 'Reporting late':
    clm1, clm2, clm3 = st.columns(3)
    start_time1 = str(clm2.time_input('from:', datetime.now(), 1))
    end_time1 = str(clm3.time_input('to:', datetime.now(), 1))
    save_add_button = clm2.button('save/add')
    if save_add_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[28] = mysum
        st.success('response added')
    save_exit_button = clm3.button('save/exit')
    if save_exit_button:
        mysum = str(calculate_time(start_time1, end_time1))
        array[28] = mysum
        finish = True
if finish is True:  # if save/exit button was pressed the code comes here
    dates = str(f"{datetime.now():%Y-%m-%d}")
    sheet.append_row(array)
    st.experimental_singleton.clear()
    st.success('response saved, you can now exit the form')
    st.stop()
