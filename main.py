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

if st.session_state.get('security_key') is None:
    st.session_state['security_key'] = 0

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
                #st.experimental_rerun()


    else:
        st.info('Note: Security key is mandatory')



if st.session_state['step'] == 1:


        with st.form(key='EmployeeForm'):

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
            reason = st.selectbox("Please choose a reason", options, key="reason")

            scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
            file = gspread.authorize(creds)
            workbook = file.open("Timesheet")
            sheet = workbook.sheet1
            sheet_url = st.secrets["private_gsheets_url"]

            details_list = []
            details = []

            if reason:
                if st.session_state["reason"]=='Customer site':
                    st.session_state["reason"]=st.columns(5)
                    clm1, clm2, clm3, clm4, clm5 = st.columns(5)
            
                if st.session_state["reason"] == 'Medical':
                    st.session_state["reason"] = st.columns(3)
                    clm1, clm2, clm3 = st.columns(3)
                    


