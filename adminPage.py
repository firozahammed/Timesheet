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

radio_selection = st.sidebar.radio('Choose an option:', ('Print Reports', 'Give Excuse'))
if radio_selection == 'Print Reports':
    st.title('Print Reports ')
    select_box_choice = st.radio('Print for:', ('All', 'Specific Employee'))
    headers = ('ID', 'name', 'date', 'customer1_visit',' customer1_name', 'customer1_country', 'customer1_location',
               'customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit',
               'customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location',
               'vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location',
               'date_of_trip','date_of_return','personal_excuse','reporting_late')
    if select_box_choice == 'All':
        clm1, clm2 = st.columns(2)

        date_from = clm1.date_input('From').strftime("%Y-%m-%d")
        date_to = clm2.date_input('To').strftime("%Y-%m-%d")

        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]
        df = pd.DataFrame(sheet.get_all_records())
        #df = df.loc[(df['date'] >= date_from) & (df['date'] <= date_to)]

        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite,engine='xlsxwriter') as writer:
            df.to_excel(writer,sheet_name='Sheet1',index=False)
            writer.save()

        download_button=st.download_button(label="Download Report",data=towrite,file_name="Report_"+date_from+".xlsx",mime="application/vnd.ms-excel")

    if select_box_choice == 'Specific Employee':
        clm1, clm2, clm3 = st.columns(3)
        ID = clm1.text_input('Enter employee ID:')
        #name = clm2.text_input(label="", value="", disabled=True)
        date_from = clm2.date_input('From').strftime("%Y-%m-%d")
        date_to = clm3.date_input('To').strftime("%Y-%m-%d")

        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]
        df = pd.DataFrame(sheet.get_all_records())
        #df = df.loc[(df['date'] >= date_from) & (df['date'] <= date_to) & (df['ID'].astype(str) == ID) ]
        df = df.loc[(df['User ID'].astype(str) == ID) ]
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1',index=False)

            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)
            
            writer.save()

        download_button = st.download_button(label="Download Report", data=towrite,
                                             file_name="Report_" + date_from + ".xlsx", mime="application/vnd.ms-excel")


elif radio_selection == 'Give Excuse':
    st.title('Give Excuse ')
    col1, col2 = st.columns(2)
    ID = col1.text_input('Enter employee ID: ')
    #name = col2.text_input(label="", value="name of ID", disabled=True)
    options = ('Customer site', 'Medical excuse', 'Vacation','Personal')
    selection = st.selectbox("Please choose a reason",options)

    if selection == 'Customer site':
        clm1, clm2, clm3, clm4, clm5 = st.columns(5)
        client_name = clm1.text_input('Client name: ')
        loc = clm3.text_input('Location:', key=1)
        country = clm2.text_input('Country:', key=3)
        start_time = clm4.date_input('From:')
        end_time = clm5.date_input('To:')
        save_add_button = clm1.button('Add')
        if save_add_button:
            array = [ID, name, selection, client_name, loc, country, start_time, end_time]
            type_to_excel(array)
            st.success('permission saved!')
        save_exit_button = clm2.button('Submit')
        if save_exit_button:
            array = [ID, name, selection, client_name, loc, country, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_excel(array)
            st.stop()
    elif selection == 'Medical excuse':
        clm1, clm2, clm3 = st.columns(3)
        hospital_name = clm1.text_input('Hospital name: ')
        start_time = clm2.date_input('From:')
        end_time = clm3.date_input('To:')
        save_add_button = clm1.button('Add')
        if save_add_button:
            array = [ID, name, selection, hospital_name, start_time, end_time]
            type_to_excel(array)
            st.success('permission saved!')
        save_exit_button = clm2.button('Submit')
        if save_exit_button:
            array = [ID, name, selection, hospital_name, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_excel(array)
            st.stop()
    elif selection == 'Vacation':
        clm1, clm2 = st.columns(2)
        start_time = clm1.date_input('From:')
        end_time = clm2.date_input('To:')
        save_add_button = clm1.button('Add')
        if save_add_button:
            array = [ID, name, selection, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_excel(array)
        save_exit_button = clm2.button('Submit')
        if save_exit_button:
            array = [ID, name, selection, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_excel(array)
            st.stop()

