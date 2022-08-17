import base64
from datetime import datetime
import datetime as dt
from datetime import date

import pyodbc
from PIL import Image

# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
file = gspread.authorize(creds)
workbook = file.open("Summary Timesheet")
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
security_key=None
st.title('Dear Employee, you have been late for today\'s attendance')
st.subheader('Please enter the security key')
security_key=st.text_input('Security key')
df = pd.DataFrame(sheet.get_all_records())
check_security_key=(security_key in df['Token'].astype(str).unique())
if check_security_key is False:
    st.error("The security key: "+security_key+" is invalid.")
else:
  #Find the row number of the employee info
  Token_col=sheet.col_values(1) 
  for cell in Token_col:
    if eval(cell.value) = eval(security_key):
        EmpInfo_RowNum=cell.row
       # emp_info=sheet.row_values(EmpInfo_RowNum)
  #Read employee Name and ID depand on the Row Number
  Emp_ID= sheet.cell(EmpInfo_RowNum, 2).value
  Emp_Name=sheet.cell(EmpInfo_RowNum, 3).value
  st.markdown("Name: "+Emp_Name+", ID: "+Emp_ID)
    
        
