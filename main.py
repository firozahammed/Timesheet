import base64

from PIL import Image

# streamlit_app.py
from datetime import date
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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


# set_bg_hack('background.png')


image = Image.open("OIP.jpg")
st.image(image)

if st.session_state.get('step') is None:
    st.session_state['step'] = 0

if st.session_state.get('security_key') is None:
    st.session_state['security_key'] = 0

if st.session_state['step'] == 0:

    with st.form(key='TokenForm'):
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]

        st.title('Please enter the security key')
        security_key = st.text_input('Security key')
        st.session_state['security_key'] = security_key
        df = pd.DataFrame(sheet.get_all_records())
        check_security_key = (security_key in df['Token'].astype(str).unique())
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:

        if security_key != "":
            if check_security_key is False:
                st.error("The security key: " + security_key + " is invalid.")
            else:
                st.session_state['step'] = 1
                st.experimental_rerun()
        else:
            st.error("Please enter the security key to proceed")

    else:
        st.info('Note: Security key is mandatory')

if st.session_state['step'] == 1:



        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]
        df = pd.DataFrame(sheet.get_all_records())
        security_key = st.session_state.get('security_key')
        df = df.loc[(df['Token'].astype(str) == str(security_key))]
        EmployeeName = df['Name'].values[0]
        EmployeeID = df['User ID'].values[0]
        EmployeeToken = df['Token'].values[0]
        ReportingTime = df['Reporting Time'].values[0]
        ReportingDate = date.today().strftime("%m/%d/%y")
        st.title("Dear " + EmployeeName + ", you have been late for today " + date.today().strftime(
            "%m/%d/%y"))
        st.text_input('Employee ID', value=EmployeeID, disabled=True)
        st.text_input('Reporting Time', value=ReportingTime, disabled=True)
        options = (
            'Customer site', 'Medical', 'Business trip', 'Personal', 'Reporting late')
        reason = st.selectbox("Please choose a reason", options)

        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]

        details_list = []
        details = []

        if reason == 'Customer site':
            NumberofClients = ('1', '2')
            SelectClients = st.selectbox("Number of clients",NumberofClients)
            if SelectClients == '1':
                clm1, clm2, clm3, clm4 = st.columns(4)
                client_name = clm1.text_input('Client name:')
                client_loc = clm2.text_input('Location:')
                from_time = clm3.time_input('From:')
                to_time = clm4.time_input('To:')
                details = ['Client:' + client_name, 'Location:' + client_loc]
                details = '\n\n'.join(details)
                add_button = clm1.button(label="Submit")
                if add_button:
                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName),
                                date.today().strftime("%m/%d/%Y"),
                                str(from_time), str(to_time),
                                reason, details]
                    sheet.append_row(details_list)
                    st.success('Your response has been submitted !')

            elif SelectClients =='2':
                clm1, clm2, clm3, clm4 = st.columns(4)
                client1_name = clm1.text_input('Client 1 (Name):')
                client1_loc = clm2.text_input('Location:')
                from1_time = clm3.time_input('From:')
                to1_time = clm4.time_input('To:')

                client2_name = clm1.text_input('Client 2 (Name):')
                client2_loc = clm2.text_input('Location:',key='Location2')
                from2_time = clm3.time_input('From:',key='From2')
                to2_time = clm4.time_input('To:',key='To2')

                details1 = ['Client 1:' + client1_name, 'Location:' + client1_loc]
                details1 = '\n\n'.join(details1)

                details2 =['Client 2:' + client2_name, 'Location:' + client2_loc]
                details2 = '\n\n'.join(details2)
                add_button = clm1.button(label="Submit")
                if add_button:
                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName),
                                    date.today().strftime("%m/%d/%Y"),
                                    str(from1_time), str(to1_time),
                                    reason, details1]
                    sheet.append_row(details_list)

                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName),
                                    date.today().strftime("%m/%d/%Y"),
                                    str(from2_time), str(to2_time),
                                    reason, details2]
                    sheet.append_row(details_list)
                    
                    st.success('Your response has been submitted!')



        elif reason == 'Medical':
            clm1, clm2, clm3 = st.columns(3)
            hospital_name = clm1.text_input('Hospital name:')
            from_time = clm2.time_input('From:')
            to_time = clm3.time_input('To:')
            save_add_button = clm1.button('Submit')
            if save_add_button:
                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName), date.today().strftime("%m/%d/%Y"),
                                    str(from_time),
                                    str(to_time), reason, 'Hospital:' + hospital_name]
                    sheet.append_row(details_list)
                    st.success('Your response has been submitted !')

        elif reason == 'Business trip':
            clm1,clm2,clm3,clm4 = st.columns(4)
            country = clm1.text_input('Country:')
            client_loc = clm2.text_input('Location:')
            from_time = clm3.time_input('From:')
            to_time = clm4.time_input('To:')
            details = ['Country:' + country,'Location:' + client_loc,]
            details = '\n\n'.join(details)
            save_add_button = clm1.button('Submit')
            if save_add_button:
                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName), date.today().strftime("%m/%d/%Y"),
                                    str(from_time),
                                    str(to_time), reason, details]
                    sheet.append_row(details_list)
                    st.success('Your response has been submitted !')

        elif reason == 'Personal':
                personal_details = st.text_area('Enter details', height=None)
                clm1, clm2 = st.columns(2)
                from_time = clm1.time_input('From:')
                to_time = clm2.time_input('To:')
                details = []
                details = personal_details
                save_add_button = clm1.button('Submit')
                if save_add_button:
                    details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName), date.today().strftime("%m/%d/%Y"),
                                    str(from_time),
                                    str(to_time), reason, details]
                    sheet.append_row(details_list)
                    st.success('Your response has been submitted !')

        elif reason == 'Reporting late':
            save_add_button = st.button('Submit')
            if save_add_button:
                details_list = [str(EmployeeToken), str(EmployeeID), str(EmployeeName), date.today().strftime("%m/%d/%Y"),
                                    str(ReportingTime),
                                    '', reason,"Reported at - "+str(ReportingTime)]
                sheet.append_row(details_list)
                st.success('Your response has been submitted !')
