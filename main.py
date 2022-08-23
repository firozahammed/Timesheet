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

#set_bg_hack('background.png')


image = Image.open("OIP.jpg")
st.image(image)


if st.session_state.get('step') is None:
    st.session_state['step'] = 0

if st.session_state['step'] == 0:
    with st.form(key = 'TokenForm'):
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]

        st.title('Please enter the security key')
        security_key = st.text_input('Security key')

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
        st.warning('Note: Security key is mandatory')

if st.session_state['step'] == 1:
    with st.form(key='EmployeeForm'):

        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Summary Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]

        df = pd.DataFrame(sheet.get_all_records())
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
            clm1, clm2, clm3, clm4, clm5 = st.columns(5)
            client_name = clm1.text_input('Client name:')
            country = clm2.text_input('Country:', key=3)
            client_loc = clm3.text_input('Location:', key=1)
            from_time = clm4.time_input('From:')
            to_time = clm5.time_input('To:')
            details = ['Client:' + client_name, 'Location:' + client_loc, 'Country:' + country]
            details = '\n\n'.join(details)
            add_button = st.form_submit_button(label="Add")
            if add_button:
                details_list = [EmployeeToken,EmployeeID,EmployeeName, date.today().strftime("%m/%d/%Y"), str(from_time), str(to_time),
                                reason, details]
                sheet.append_row(details_list)
                st.success('Successfully added!')


            elif reason == 'Medical':
                clm1, clm2, clm3 = st.columns(3)
                hospital_name = clm1.text_input('Hospital name:')
                from_time = clm4.time_input('From:')
                to_time = clm5.time_input('To:')
                save_add_button = clm1.button('Add')
                if save_add_button:
                    details_list = [EmployeeToken,EmployeeID,EmployeeName, date.today().strftime("%m/%d/%Y"), str(from_time),
                                    str(to_time), reason, 'Hospital:' + hospital_name]
                    sheet.append_row(details_list)
                    st.success('Successfully added!')
                    st.session_state['step'] = 1


            elif reason == 'Business trip':
                clm1, clm2 = st.columns(2)
                from_time = clm1.time_input('From:')
                to_time = clm2.time_input('To:')
                save_add_button = clm1.button('Add')
                if save_add_button:
                    details_list = [EmployeeToken,EmployeeID,EmployeeName, date.today().strftime("%m/%d/%Y"), str(from_time),
                                    str(to_time), reason]
                    sheet.append_row(details_list)
                    st.success('Successfully added!')
                    st.session_state['step'] = 1



            elif reason == 'Personal':

                personal_details = st.text_area('Enter details', height=None)
                clm1, clm2 = st.columns(2)
                from_time = clm1.time_input('From:')
                to_time = clm2.time_input('To:')
                details = []
                details = personal_details
                save_add_button = clm1.button('Add')
                if save_add_button:
                    details_list = [EmployeeToken,EmployeeID,EmployeeName, date.today().strftime("%m/%d/%Y"), str(from_time),
                                    str(to_time), reason, details]
                    sheet.append_row(details_list)
                    st.success('Successfully added!')
                    st.session_state['step'] = 1



