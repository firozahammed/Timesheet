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
st.title('Please enter the security key')
st.text_input('Security key',security_key)
selection = security_key
