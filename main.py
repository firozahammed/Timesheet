import base64


from PIL import Image

# streamlit_app.py

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
placeholder = st.empty()
with placeholder.container():

    st.title('Please enter the security key')
    security_key = st.text_input(placeholder="Security key")
    df = pd.DataFrame(sheet.get_all_records())
    check_security_key = (security_key in df['Token'].astype(str).unique())
    submit_button = st.button("Submit")

    if submit_button:

        if security_key!="":
            if check_security_key is False:
                st.error("The security key: " + security_key + " is invalid.")
        #placeholder.empty()

            else:
                placeholder.empty()
        else:
            st.error("Please enter the security key")

#placeholder = st.empty()
#placeholder.title("Initial text")

#with placeholder.container():

#    st.write("This is elemnet 1")
#    st.write("This is element 2")



#with st.empty():
#    i=30
#    while i>0:
#        st.write(f"{i} seconds left")
#        time.sleep(1)
#        i=i-1

#    st.write("Time's up !")




