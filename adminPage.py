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
        date_from = clm1.date_input('From')
        date_to = clm2.date_input('To')


        # Create a connection object.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        conn = connect(credentials=credentials)

        # Perform SQL query on the Google Sheet.
        # Uses st.cache to only rerun when the query changes or after 10 min.
        @st.cache(ttl=600)
        def run_query(query):
            rows = conn.execute(query, headers=1)
            rows = rows.fetchall()
            return rows

        #customer_name=["Ali"]
        sheet_url = st.secrets["private_gsheets_url"]
        #rows = run_query(f'SELECT * FROM "{sheet_url}" WHERE ID={id_num}')
        #rows = run_query(f'SELECT * FROM "{sheet_url}" WHERE name={customer_name}')
        rows = run_query(df[df['name'].str.contains('Ali')])
        #Print results.
        for row in rows:
            st.write(rows)

        output = BytesIO()

        # Write files to in-memory strings using BytesIO
        # See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Hello')
        workbook.close()
        download_button=st.download_button(label="Download Report",data=output.getvalue(),file_name="workbook.xlsx",mime="application/vnd.ms-excel")

