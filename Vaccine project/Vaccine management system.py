import streamlit as st
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import hashlib


mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client.vaccine_management


users = {
    "admin": {"password": hashlib.sha256("adminpass".encode()).hexdigest(), "role": "admin"},
    "staff": {"password": hashlib.sha256("staffpass".encode()).hexdigest(), "role": "staff"}
}


if 'patients' not in st.session_state:
    st.session_state.patients = list(db.patients.find({}, {'_id': 0}))

if 'vaccinations' not in st.session_state:
    st.session_state.vaccinations = list(db.vaccinations.find({}, {'_id': 0}))

if 'vaccines' not in st.session_state:
    st.session_state.vaccines = [
        "Pneumococcal",
        "Polio (Poliomyelitis)",
        "Rotavirus",
        "RSV (Respiratory Syncytial Virus)",
        "Rubella (German Measles)",
        "Shingles (Herpes Zoster)",
        "Tetanus (Lockjaw)",
        "Whooping Cough (Pertussis)"
    ]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    return username in users and users[username]['password'] == hash_password(password)

def get_user_role(username):
    return users[username]['role']

def register_patient(name, age, gender, address, phone, email):
    patient_id = len(st.session_state.patients) + 1
    patient = {
        'Patient ID': patient_id,
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Address': address,
        'Phone': phone,
        'Email': email
    }
    st.session_state.patients.append(patient)
    db.patients.insert_one(patient)
    st.success(f"Patient {name} registered successfully with ID {patient_id}")

def record_vaccination(patient_id, vaccine_name, date):
    date = datetime.combine(date, datetime.min.time())
    patient = next((p for p in st.session_state.patients if p['Patient ID'] == patient_id), None)
    if patient:
        vaccination = {
            'Patient ID': patient_id,
            'Patient Name': patient['Name'],
            'Vaccine Name': vaccine_name,
            'Date': date,
            'Administered': True
        }
        st.session_state.vaccinations.append(vaccination)
        db.vaccinations.insert_one(vaccination)
        st.success(f"Vaccination recorded successfully for {patient['Name']} (ID: {patient_id})")
    else:
        st.error("Invalid Patient ID")

def view_patients(search_query=""):
    if st.session_state.patients:
        patients = st.session_state.patients
        if search_query:
            patients = [p for p in patients if search_query.lower() in p['Name'].lower() or search_query in str(p['Patient ID'])]
        df = pd.DataFrame(patients)
        st.write(df)
    else:
        st.write("No patient records available.")

def view_vaccinations(search_query=""):
    if st.session_state.vaccinations:
        vaccinations = st.session_state.vaccinations
        if search_query:
            vaccinations = [v for v in vaccinations if search_query.lower() in v['Patient Name'].lower() or search_query in str(v['Patient ID'])]
        df = pd.DataFrame(vaccinations)
        st.write(df)
    else:
        st.write("No vaccination records available.")

def check_vaccination_status(patient_id):
    vaccinations = [v for v in st.session_state.vaccinations if v['Patient ID'] == patient_id]
    return vaccinations

def add_new_vaccine(vaccine_name):
    if vaccine_name in st.session_state.vaccines:
        st.warning(f"The vaccine '{vaccine_name}' already exists.")
    else:
        st.session_state.vaccines.append(vaccine_name)
        st.success(f"New vaccine '{vaccine_name}' added successfully.")


st.title("Vaccine Management System")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


page_bg_img = '''
<style>
body {
    background-image: url("https://www.publicdomainpictures.net/pictures/320000/velka/vaccination-concept.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")
else:
    user_role = get_user_role(st.session_state.username)
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({user_role})")

    
    st.sidebar.subheader("Menu")
    menu_register = ["Register Patient", "Register Vaccine"]
    if user_role == "admin":
        menu_register.append("Add New Vaccine")

    menu_records = ["View Patients", "View Vaccinations"]
    menu_manage = ["Check Vaccination Status", "Logout"]
    if user_role == "admin":
        menu_manage.insert(0, "Edit Patient Info")

    selected_menu = st.sidebar.radio("Select an option", ["Register", "Records", "Manage"])
    
    if selected_menu == "Register":
        menu = st.sidebar.radio("Register Menu", menu_register)

    elif selected_menu == "Records":
        menu = st.sidebar.radio("Records Menu", menu_records)

    elif selected_menu == "Manage":
        menu = st.sidebar.radio("Manage Menu", menu_manage)
    
    
    if menu == "Add New Vaccine" and user_role == "admin":
        st.subheader("Add New Vaccine")
        new_vaccine_name = st.text_input("Enter the name of the new vaccine")
        if st.button("Add"):
            add_new_vaccine(new_vaccine_name)

    elif menu == "Register Patient":
        st.subheader("Register New Patient")
        name = st.text_input("Patient Name")
        age = st.number_input("Patient Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        address = st.text_input("Address")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        if st.button("Register"):
            register_patient(name, age, gender, address, phone, email)

    elif menu == "Register Vaccine":
        st.subheader("Register Vaccine")
        patient_id = st.number_input("Patient ID", min_value=1)
        vaccine_name = st.selectbox("Vaccine Name", st.session_state.vaccines)
        date = st.date_input("Date")
        if st.button("Register"):
            record_vaccination(patient_id, vaccine_name, date)

    elif menu == "View Patients":
        st.subheader("Patient Records")
        search_query = st.text_input("Search by Patient Name or ID")
        view_patients(search_query)

    elif menu == "View Vaccinations":
        st.subheader("Vaccination Records")
        search_query = st.text_input("Search by Patient Name or ID")
        view_vaccinations(search_query)

    elif menu == "Check Vaccination Status":
        st.subheader("Check Vaccination Status")
        patient_id = st.number_input("Patient ID", min_value=1)
        if st.button("Check"):
            vaccinations = check_vaccination_status(patient_id)
            if vaccinations:
                df = pd.DataFrame(vaccinations)
                st.write(df)
            else:
                st.write(f"No vaccinations found for Patient ID {patient_id}")

    elif menu == "Edit Patient Info" and user_role == "admin":
        st.subheader("Edit Patient Information")
        patient_id = st.number_input("Patient ID", min_value=1)
        patient = next((p for p in st.session_state.patients if p['Patient ID'] == patient_id), None)
        if patient:
            name = st.text_input("Patient Name", value=patient['Name'])
            age = st.number_input("Patient Age", min_value=0, max_value=120, value=patient['Age'])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient['Gender']))
            address = st.text_input("Address", value=patient['Address'])
            phone = st.text_input("Phone Number", value=patient['Phone'])
            email = st.text_input("Email", value=patient['Email'])
            if st.button("Update"):
                patient['Name'] = name
                patient['Age'] = age
                patient['Gender'] = gender
                patient['Address'] = address
                patient['Phone'] = phone
                patient['Email'] = email
                db.patients.update_one({'Patient ID': patient_id}, {'$set': patient})
                st.success(f"Patient ID {patient_id} information updated successfully.")
        else:
            st.error("Invalid Patient ID")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
