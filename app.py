import streamlit as st
import time
import requests
from pdf2image import convert_from_bytes
import sqlite3
import pandas as pd

# --- DB Functions ---
def init_db():
    conn = sqlite3.connect("medical_records.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, address TEXT, medicines TEXT, directions TEXT, refill TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS patient_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, vaccination_status TEXT, medical_problems TEXT, has_insurance TEXT
    )""")
    conn.commit()
    conn.close()

def insert_prescription(name, address, medicines, directions, refill):
    conn = sqlite3.connect("medical_records.db")
    c = conn.cursor()
    c.execute("INSERT INTO prescriptions (name, address, medicines, directions, refill) VALUES (?, ?, ?, ?, ?)",
              (name, address, medicines, directions, refill))
    conn.commit()
    conn.close()

def insert_patient_details(name, phone, vaccination_status, medical_problems, has_insurance):
    conn = sqlite3.connect("medical_records.db")
    c = conn.cursor()
    c.execute("INSERT INTO patient_details (name, phone, vaccination_status, medical_problems, has_insurance) VALUES (?, ?, ?, ?, ?)",
              (name, phone, vaccination_status, medical_problems, has_insurance))
    conn.commit()
    conn.close()

def fetch_all(table):
    conn = sqlite3.connect("medical_records.db")
    c = conn.cursor()
    records = c.execute(f"SELECT * FROM {table}").fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    df = pd.DataFrame(records, columns=columns)
    return df

# Initialize database
init_db()

# --- FastAPI request ---
def make_request(file, doc_type):
    files = {"file": file.getvalue()}
    data = {"file_format": doc_type}
    try:
        res = requests.post("http://localhost:8000/extract_from_doc", files=files, data=data)
        if res.status_code == 200:
            return res.json()
        else:
            st.error("Extraction failed. Check the backend route.")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Medical History Extractor", layout="wide")
st.title("🩺 Medical Data Extractor")

page = st.sidebar.selectbox("Choose a page", ["Upload", "Dashboard"])

if page == "Upload":
    file = st.file_uploader("Upload PDF", type="pdf")
    col3, col4 = st.columns(2)

    with col3:
        file_format = st.radio(label="Select type of document", options=["prescription", "patient_details"], horizontal=True)

    with col4:
        if file and st.button("Upload PDF", type="primary"):
            bar = st.progress(50)
            time.sleep(1)
            bar.progress(100)
            data = make_request(file, file_format)
            if data:
                st.session_state["extracted"] = data

    if file:
        pages = convert_from_bytes(file.getvalue())
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded File Preview")
            st.image(pages[0])

        with col2:
            if "extracted" in st.session_state:
                st.subheader("Extracted Details")
                extracted = st.session_state["extracted"]

                if file_format == "prescription":
                    name = st.text_input("Name", value=extracted.get("patient_name", ""))
                    address = st.text_input("Address", value=extracted.get("patient_address", ""))
                    medicines = st.text_input("Medicines", value=extracted.get("medicines", ""))
                    directions = st.text_input("Directions", value=extracted.get("directions", ""))
                    refill = st.text_input("Refill", value=extracted.get("refill", ""))

                    if st.button("Submit", type="primary"):
                        insert_prescription(name, address, medicines, directions, refill)
                        st.success("✅ Prescription saved successfully.")
                        del st.session_state["extracted"]

                elif file_format == "patient_details":
                    name = st.text_input("Name", value=extracted.get("patient_name", ""))
                    phone = st.text_input("Phone No.", value=extracted.get("phone_no", ""))
                    vacc_status = st.text_input("Vaccination Status", value=extracted.get("vaccination_status", ""))
                    med_problems = st.text_input("Medical Problems", value=extracted.get("medical_problems", ""))
                    has_insurance = st.text_input("Has Insurance", value=extracted.get("has_insurance", ""))

                    if st.button("Submit", type="primary"):
                        insert_patient_details(name, phone, vacc_status, med_problems, has_insurance)
                        st.success("✅ Patient details saved successfully.")
                        del st.session_state["extracted"]

elif page == "Dashboard":
    st.header("📋 Stored Medical Records")

    st.subheader("Prescriptions")
    pres_df = fetch_all("prescriptions")
    st.dataframe(pres_df, use_container_width=True)

    st.subheader("Patient Details")
    details_df = fetch_all("patient_details")
    st.dataframe(details_df, use_container_width=True)



