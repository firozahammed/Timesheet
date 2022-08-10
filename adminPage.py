import csv
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
radio_selection = st.sidebar.selectbox('choose an option:', ('print reports', 'give permission', 'give privilege'))
if radio_selection == 'print reports':
    select_box_choice = st.selectbox('who to print for:', ('all', 'certain employee'))
    headers = ('ID', 'name', 'date', 'customer1_visit',' customer1_name', 'customer1_country', 'customer1_location',
               'customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit',
               'customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location',
               'vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location',
               'date_of_trip','date_of_return','personal_excuse','reporting_late')
    if select_box_choice == 'all':
        clm1, clm2 = st.columns(2)
        date_from = clm1.date_input('from')
        date_to = clm2.date_input('to')
        sheet_url = st.secrets["private_gsheets_url"]
        import pandas as pd
        import base64
        import io
        download_button=clm1.button('downlaod report', f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>')
        if download_button:
            df = pd.DataFrame(vals, columns=["ID",'name','date','total hours','total office hours','customer1_visit','customer1_name','customer1_country','customer1_location','customer2_visit','customer2_name','customer2_country','customer2_location','customer3_visit','customer3_name','customer3_country','customer3_location','hospital_visit','hospital_location','vendor1_visit','vendor1_name','vendor2_visit','vendor2_name','business_trip_country','trip_location','date_of_trip','date_of_return','personal_excuse',"reporting_late"])
            towrite = io.BytesIO()
            downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode()  # some strings
            st.markdown(linko, unsafe_allow_html=True)
    elif select_box_choice == 'certain employee':
        clm1, clm2, clm3, clm4 = st.columns(4)
        ID = clm1.text_input('enter employee ID:')
        name = clm2.text_input(label="", value="asdasd", disabled=True)
        date_from = clm3.date_input('from')
        date_to = clm4.date_input('to')
        download_button = clm1.button('download report')
        if download_button:
            conn = init_connection()
            cur = conn.cursor()
            result = cur.execute('select * from attendance where date >= ? AND date <= ? AND ID = ?', date_from, date_to,ID)
            rows = result.fetchall()
            with open('report '+str(date_from)+' '+str(date_to)+'.csv', 'a') as f:
                # using csv.writer method from CSV package
                dw = csv.DictWriter(f, delimiter=',',
                                    fieldnames=headers)
                dw.writeheader()
                for row in rows:
                    write = csv.writer(f)
                    write.writerow(row)
            st.success('report downloaded!')

elif radio_selection == 'give permission':
    col1, col2 = st.columns(2)
    ID = col1.text_input('enter employee ID: ')
    name = col2.text_input(label="", value="name of ID", disabled=True)
    options = ('Customer site', 'Medical excuse', 'Vacation')
    selection = st.selectbox("please choose a reason",
                             options)

    if selection == 'Customer site':
        clm1, clm2, clm3, clm4, clm5 = st.columns(5)
        client_name = clm1.text_input('Client name: ')
        loc = clm3.text_input('location:', key=1)
        country = clm2.text_input('country:', key=3)
        start_time = clm4.date_input('from:')
        end_time = clm5.date_input('to:')
        save_add_button = clm4.button('save/add')
        if save_add_button:
            array = [ID, name, selection, client_name, loc, country, start_time, end_time]
            type_to_csv(array)
            st.success('permission saved!')
        save_exit_button = clm5.button('save/exit')
        if save_exit_button:
            array = [ID, name, selection, client_name, loc, country, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_csv(array)
            st.stop()
    elif selection == 'Medical excuse':
        clm1, clm2, clm3 = st.columns(3)
        hospital_name = clm1.text_input('Hospital name: ')
        start_time = clm2.date_input('from:')
        end_time = clm3.date_input('to:')
        save_add_button = clm2.button('save/add')
        if save_add_button:
            array = [ID, name, selection, hospital_name, start_time, end_time]
            type_to_csv(array)
            st.success('permission saved!')
        save_exit_button = clm3.button('save/exit')
        if save_exit_button:
            array = [ID, name, selection, hospital_name, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_csv(array)
            st.stop()
    elif selection == 'Vacation':
        clm1, clm2, clm3 = st.columns(3)
        start_time = clm2.date_input('from:')
        end_time = clm3.date_input('to:')
        save_add_button = clm2.button('save/add')
        if save_add_button:
            array = [ID, name, selection, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_csv(array)
        save_exit_button = clm3.button('save/exit')
        if save_exit_button:
            array = [ID, name, selection, start_time, end_time]
            st.success('permission saved , you can exit the site')
            type_to_csv(array)
            st.stop()

elif radio_selection == 'give privilege':
    col1, col2 = st.columns(2)
    ID = col1.text_input('enter employee ID that you want to give privilege to : ')
    col2.text_input(label="", value="asdasd", disabled=True)
    col2.button('confirm')
