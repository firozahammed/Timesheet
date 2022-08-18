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
import datetime as dt
import streamlit as st
import numpy as np
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread as gs
import datetime
from datetime import timedelta
import time
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

radio_selection = st.sidebar.radio('Choose an option:', ('Print Reports', 'Employee Exemption'))
if radio_selection == 'Print Reports':
    st.title('Print Reports ')
    select_box_choice = st.radio('Print:', ('Daily', 'Summary'))
    headers = ('ID', 'name', 'date', 'customer1_visit',' customer1_name', 'customer1_country', 'customer1_location',
               'customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit',
               'customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location',
               'vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location',
               'date_of_trip','date_of_return','personal_excuse','reporting_late')
    if select_box_choice == 'Daily':
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

            # Autofit excel column header
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)


            writer.save()

        download_button=st.download_button(label="Download Report",data=towrite,file_name="Report_"+date_from+".xlsx",mime="application/vnd.ms-excel")

    if select_box_choice == 'Summary':
        clm1, clm2, clm3 = st.columns(3)
        ID = clm1.text_input('Enter employee ID:')
        #name = clm2.text_input(label="", value="", disabled=True)
        date_from = clm2.date_input('From').strftime("%m/%d/%Y")
        date_to = clm3.date_input('To').strftime("%m/%d/%Y")

        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Attendance")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]
        df = pd.DataFrame(sheet.get_all_records())
        #df = df.loc[(df['date'] >= date_from) & (df['date'] <= date_to) & (df['ID'].astype(str) == ID) ]
        #df['Date']=pd.to_datetime(df['Date'])
        #df.groupby([pd.Grouper(key='Date')])['Total Time'].sum()
        #df['Total Time']=pd.to_datetime(df['Total Time'],format='%H:%M:%S',errors='ignore').dt.time
        #df['Total Time'] = pd.to_datetime(df['Total Time'].astype(str)).dt.strftime('%H:%M:%S')
        #df['Total Time'] = df['Total Time'].dt.strptime('%H:%M:%S')
        #df['Total Time']=pd.to_datetime(df['Total Time'],format='%H:%M:%S',errors='ignore').dt.time
        #df['Total Time'] = df['Total Time'].dt.total_seconds()
        #df['Total Time'] = pd.to_datetime(df['Total Time'])
        #datetime = datetime.datetime.strptime(df['Total Time'],"%H:%M:%S")
        #df['Total Time'] = df['Total Time'] - datetime.datetime(2022,8,18)
        #seconds = df['Total Time'].total_seconds()

        df['Total Time'] = (pd.to_timedelta(df['Total Time']).astype('timedelta64[s]').astype(int))/3600

        df['Date']= pd.to_datetime(df['Date'], format='%m/%d/%Y')

        #df['Date'] = df['Date'].strftime("%m/%d/%Y")
        df = df.loc[(df['Date'] >= "8/1/2022") & (df['Date'] <= "8/2/2022")]
        df = df.groupby(['Employee ID',pd.to_datetime(df['Date'], format='%m/%d/%Y')],as_index=False)['Total Time'].sum()
        df




        #df=df.groupby(['Employee ID'])['Total Time'].sum()

        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1',index=False)

            #Autofit excel column header
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)

            writer.save()

        download_button = st.download_button(label="Download Report", data=towrite,
                                             file_name="Report_" + date_from + ".xlsx", mime="application/vnd.ms-excel")


elif radio_selection == 'Employee Exemption':
    st.title('Employee Exemption')
    col1, col2 = st.columns(2)

    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
    file = gspread.authorize(creds)
    workbook = file.open("Employee Exemption")
    sheet = workbook.sheet1
    sheet_url = st.secrets["private_gsheets_url"]

    exemption_list=[]
    details=[]
    ID = col1.text_input('Enter employee ID: ')
    #name = col2.text_input(label="", value="name of ID", disabled=True)
    options = ('Customer site', 'Medical', 'Vacation','Personal')
    reason = st.selectbox("Please choose a reason",options)

    if reason == 'Customer site':
        clm1, clm2, clm3, clm4, clm5 = st.columns(5)
        client_name = clm1.text_input('Client name:')
        client_loc = clm3.text_input('Location:', key=1)
        country = clm2.text_input('Country:', key=3)
        from_date = clm4.date_input('From:').strftime("%m/%d/%Y")
        to_date = clm5.date_input('To:').strftime("%m/%d/%Y")
        details=['Client:'+client_name,'Location:'+client_loc,'Country:'+country]
        details='\n\n'.join(details)
        save_add_button = clm1.button('Add')
        if save_add_button:
            exemption_list = [ID,str(from_date),str(to_date), reason,details]
            sheet.append_row(exemption_list)
            st.success('Successfully added!')
            st.stop()
    elif reason == 'Medical':
        clm1, clm2, clm3 = st.columns(3)
        hospital_name = clm1.text_input('Hospital name:')
        from_date = clm2.date_input('From:').strftime("%m/%d/%Y")
        to_date = clm3.date_input('To:').strftime("%m/%d/%Y")
        save_add_button = clm1.button('Add')
        if save_add_button:
            exemption_list = [ID, str(from_date), str(to_date), reason,'Hospital:'+hospital_name]
            sheet.append_row(exemption_list)
            st.success('Successfully added!')
            st.stop()

    elif reason == 'Vacation':
        clm1, clm2 = st.columns(2)
        start_time = clm1.date_input('From:').strftime("%m/%d/%Y")
        end_time = clm2.date_input('To:').strftime("%m/%d/%Y")
        save_add_button = clm1.button('Add')
        if save_add_button:
                exemption_list = [ID, str(from_date), str(to_date), reason]
                sheet.append_row(exemption_list)
                st.success('Successfully added!')
                st.stop()


    elif reason == 'Personal':

        personal_details = st.text_area('Enter details',height=None)
        clm1, clm2 = st.columns(2)
        from_date = clm1.date_input('From:').strftime("%m/%d/%Y")
        to_date = clm2.date_input('To:').strftime("%m/%d/%Y")
        details = []
        details = personal_details
        save_add_button = clm1.button('Add')
        if save_add_button:
            exemption_list = [ID, str(from_date), str(to_date), reason, details]
            sheet.append_row(exemption_list)
            st.success('Successfully added!')
            st.stop()
