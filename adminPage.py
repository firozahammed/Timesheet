import csv
import pandas as pd
import base64
import io
import xlsxwriter
from io import BytesIO
import pyodbc
from PIL import Image
import streamlit as st
import base64
import datetime
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread as gs
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
radio_selection = st.sidebar.selectbox('Choose an option:', ('---','Print Reports', 'Give Exception', 'Grant Privilege'))
if radio_selection == 'Print Reports':
    st.title('Print Reports ')
    select_box_choice = st.selectbox('Print for:', ('--','All', 'Specific Employee'))
    headers = ('ID', 'name', 'date', 'customer1_visit',' customer1_name', 'customer1_country', 'customer1_location',
               'customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit',
               'customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location',
               'vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location',
               'date_of_trip','date_of_return','personal_excuse','reporting_late')
    if select_box_choice == 'All':
        clm1, clm2 = st.columns(2)

        date_from = clm1.date_input('From').strftime("%Y-%m-%d")
        date_to = clm2.date_input('To').strftime("%Y-%m-%d")

        #date_from = datetime.strptime(clm1.date_input('From'),'%Y-%m-%d')
        #date_to = datetime.strptime(clm2.date_input('To'),'%Y-%m-%d')





        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]
        df = pd.DataFrame(sheet.get_all_records())
        df.loc[(df['date'] >= date_from) & (df['date'] <= date_to)]



        towrite = io.BytesIO()
        downloaded_file=df.to_excel(towrite,encoding='utf-8',index=False,header=True)
        towrite.seek(0)
        b64=base64.b64encode(towrite.read()).decode()
       # Write files to in-memory strings using BytesIO
        #See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
        #workbook = xlsxwriter.Workbook(df, {'in_memory': True})
        #worksheet = workbook.add_worksheet()
        #worksheet.write(df)
        #workbook.close()
        
        download_button=st.download_button(label="Download Report",data=df,file_name="workbook.xlsx",mime="application/vnd.ms-excel")
