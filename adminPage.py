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

def fetch_data(date_from,date_to,rows):
    with open('report ' + str(date_from) + ' ' + str(date_to) + '.csv', 'a') as f:
        # using csv.writer method from CSV package
        dw = csv.DictWriter(f, delimiter=',',
                            fieldnames=headers)
        dw.writeheader()
        for row in rows:
            write = csv.writer(f)
            write.writerow(row)





# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],)
conn = connect(credentials=credentials)

def type_to_csv(array):
    with open('permissions.csv', 'a') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(array)


@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


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
st.title('Welcome to the admin page ')
radio_selection = st.sidebar.selectbox('Choose an option:', ('Print Reports', 'Give Exception', 'Grant Privilege'))
if radio_selection == 'print reports':
    select_box_choice = st.selectbox('who to print for:', ('all', 'certain employee'))
    headers = ('ID', 'name', 'date', 'customer1_visit',' customer1_name', 'customer1_country', 'customer1_location',
               'customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit',
               'customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location',
               'vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location',
               'date_of_trip','date_of_return','personal_excuse','reporting_late')
    if select_box_choice == 'all':
        clm1, clm2 = st.columns(2)
        date_from = clm1.date_input('From')
        date_to = clm2.date_input('To')
        sheet_url = st.secrets["private_gsheets_url"]


        output = BytesIO()

        # Write files to in-memory strings using BytesIO
        # See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Hello')
        workbook.close()
if date_to:
      download_button=st.download_button(label="Download Excel workbook",data=output.getvalue(),file_name="workbook.xlsx",mime="application/vnd.ms-excel")

