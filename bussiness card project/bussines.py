
import re
from PIL import Image
import pytesseract
import streamlit as st
import mysql.connector
import pandas as pd

def insert_data(data):
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bussines_card"
        )
        cursor = cnx.cursor()

        insert_query = "INSERT INTO card_details (card_holder_name, designation, mobile_number, email_address, website_url, area, city, state, pin_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data)
        cnx.commit()
        

    except Exception as e:
        st.write("Error: Failed to insert data into the database.")
        st.write(e)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def main():
    st.title('BizCardX: Extract Business Card Data with OCR')
    st.write("Upload an image of a business card to extract relevant information.")

    image = st.file_uploader('Upload Image', type=['jpg', 'jpeg', 'png'])

    if image is not None:
        img = Image.open(image)
        processed_image = img.resize((800, 600))
        txt = pytesseract.image_to_string(processed_image)

        
        st.write("Extracted Text:")
        
        st.write(txt)

        
        email_pattern = r'[\w\.-]+@[\w\.-]+'
        phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        url_pattern = r'\b(?:https?://|www\.)\S+\b'
        pin_code_pattern = r'\b\d{6}\b'
        lines = txt.split('\n')
        card_holder_name = lines[0]
        designation = lines[1]
        phone_number = re.search(phone_pattern, txt).group() if re.search(phone_pattern, txt) else ''
        email_address = re.search(email_pattern, txt).group() if re.search(email_pattern, txt) else ''
        website_url = re.search(url_pattern, txt).group() if re.search(url_pattern, txt) else ''
        pin_code_value = re.search(pin_code_pattern, txt).group() if re.search(pin_code_pattern, txt) else ''
        address = lines[5]

        
        st.write("Manual Adjustments:")
        card_holder_name = st.text_input('Card Holder Name', card_holder_name)
        designation = st.text_input('Designation', designation)
        phone_number = st.text_input('Phone Number', phone_number)
        email_address = st.text_input('Email', email_address)
        website_url = st.text_input('Website', website_url)
        address = st.text_input('Address', address)
        
        area = st.text_input('Area', '')
        city = st.text_input('City', '')
        state = st.text_input('State', '')
        pin_code = st.text_input('Pin Code', pin_code_value)

        
        insert_button = st.button('Insert Data')
        
        if insert_button:
            
            data = (card_holder_name, designation, phone_number, email_address, website_url, area, city, state, pin_code)
            insert_data(data)
            st.write("Data inserted successfully!")


showdata_button = st.button('show_data')


if showdata_button:
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bussines_card"
        )
        cursor = cnx.cursor()

        query = 'SELECT * FROM card_details'
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            column_names = [desc[0] for desc in cursor.description]
            
            df = pd.DataFrame(data, columns=column_names)
            
            st.write("Data from card_details:")
            st.dataframe(df)

    except Exception as e:
        st.write("Error: Failed to fetch and display data from the database.")
        st.write(e)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()




delete_button = st.button('Delete')

if delete_button:
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bussines_card"
        )
        cursor = cnx.cursor()

        delete_query = 'DELETE FROM card_details'
        cursor.execute(delete_query)
        cnx.commit()

        st.write("Data deleted successfully!")

    except Exception as e:
        st.write("Error: Failed to delete data from the database.")
        st.write(e)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

 
def updatedata(data,id):
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database=" bussines_card"
        )
        cursor = cnx.cursor()
        print(id)
        insert_query = "Update card_details set card_holder_name ='"+data[0]+"', designation='"+data[1]+"', mobile_number="+data[2]+", email_address='"+data[3]+"', website_url='"+data[4]+"', area='"+data[5]+"', city='"+data[6]+"', state='"+data[7]+"', pin_code='"+data[8]+"' WHERE id = '"+str(id)+"'"
        cursor.execute(insert_query)
        cnx.commit()
        

    except Exception as e:
        st.write("Error: Failed to update data into the database.")
        st.write(e)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()



id_input = st.text_input('Enter ID')
fetch_button = st.button('Fetch Data')
if fetch_button:
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bussines_card"
        )
        cursor = cnx.cursor()

        query ='SELECT * FROM card_details where id ="'+str(id_input)+'"'
        cursor.execute(query, )
        data = cursor.fetchall()


        if data:
            print(data)
            st.session_state['id'] = data[0][0]
            st.session_state['card_holder_name'] = data[0][1]
            st.session_state['designation'] = data[0][2]
            st.session_state['phone_number'] = data[0][3]
            st.session_state['email_address'] = data[0][4]
            st.session_state['website_url'] = data[0][5]
            st.session_state['address'] = data[0][6]
            st.session_state['area'] = data[0][7]
            st.session_state['city'] = data[0][8]
            st.session_state['state'] = data[0][9]

                
            
            

        else:
            st.write('data not found')


    except Exception as e:
        st.write("Error: Failed to fetch and display data from the database.")
        st.write(e)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


with st.form("my-form"):
    
    card_holder_name = st.text_input('Card Holder Name', key='card_holder_name')
    designation = st.text_input('Designation', key='designation')
    phone_number = st.text_input('Phone Number', key='phone_number')
    email_address = st.text_input('Email', key='email_address')
    website_url = st.text_input('Website', key='website_url')
    address = st.text_input('Address', key='address')
    
    area = st.text_input('Area', key='area')
    city = st.text_input('City', key='city')
    state = st.text_input('State', key='state')
    pin_code = st.text_input('Pin Code', '')


    submit_button = st.form_submit_button("Submit question")
    if submit_button:
        data = (card_holder_name, designation, phone_number, email_address, website_url, area, city, state, pin_code)
        updatedata(data,st.session_state['id'])
        st.write("Data updated successfully!")

if __name__ == "__main__":
    main()
