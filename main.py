import base64


from PIL import Image

# streamlit_app.py
from datetime import date
from datetime import datetime
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
file = gspread.authorize(creds)
workbook = file.open("Summary Timesheet")
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



TokenForm = st.form()
EmployeeForm = st.form()

TokenContainer = st.empty()
FormContainer = st.empty()
TokenContainerFlag = False

if 'TokenSession' not in st.session_state:
    st.session_state['TokenSession'] = 0


if TokenContainerFlag is False:
    with TokenContainer.container():
      with TokenForm:
            TokenForm.title('Please enter the security key')
            security_key = TokenForm.text_input('Security key')
            df = pd.DataFrame(sheet.get_all_records())
            check_security_key = (security_key in df['Token'].astype(str).unique())
            submit_button = TokenForm.form_submit_button(label="Submit")

            if submit_button:

                if security_key != "":
                    if check_security_key is False:
                        st.error("The security key: " + security_key + " is invalid.")
                    else:

                        TokenContainer.empty()
                        TokenContainerFlag = True
                        st.session_state['TokenSession'] += 1


            else:
                 st.warning('Note: Security key is mandatory')

if TokenContainerFlag is True:
    with st.container():
       with EmployeeForm: 
        df = pd.DataFrame(sheet.get_all_records())
        df = df.loc[(df['Token'].astype(str) == str(security_key))]
        EmployeeName = df['Name'].values[0]
        EmployeeID = df['User ID'].values[0]
        EmployeeToken = df['Token'].values[0]
        ReportingTime = df['Reporting Time'].values[0]
        ReportingDate = date.today().strftime("%m/%d/%y")
        EmployeeForm.title("Dear " + EmployeeName + ", you have been late for today " + date.today().strftime("%m/%d/%y"))
        EmployeeForm.text_input('Employee ID', value=EmployeeID, disabled=True)
        EmployeeForm.text_input('Reporting Time', value=ReportingTime, disabled=True)
        options = ('Customer visit', 'Medical', 'Vendor visit', 'Business trip', 'Personal', 'Reporting late')
        reason = EmployeeForm.selectbox("Please choose a reason", options)

        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scopes=scopes)
        file = gspread.authorize(creds)
        workbook = file.open("Timesheet")
        sheet = workbook.sheet1
        sheet_url = st.secrets["private_gsheets_url"]

        exemption_list = []
        details = []

        if reason == 'Customer visit':
            clm1, clm2, clm3, clm4, clm5 = st.columns(5)
            client_name = clm1.text_input('Client name:')
            client_loc = clm3.text_input('Location:', key=1)
            country = clm2.text_input('Country:', key=3)
            from_time = clm4.time_input('From:', datetime.now(), 1)
            to_time = clm5.time_input('To:', datetime.now(), 1)
            details = ['Client:' + client_name, 'Location:' + client_loc, 'Country:' + country]
            details = '\n\n'.join(details)
            save_add_button = clm1.button('Add')
            if save_add_button:
                details_list = [str(EmployeeToken),str(EmployeeID), str(EmployeeName), str(ReportingDate), str(from_time), str(to_time),
                                reason, details]
                sheet.append_row(details_list)
                # st.success('Successfully added!')
                st.write(details_list)
                st.stop()

        else:
            pass

