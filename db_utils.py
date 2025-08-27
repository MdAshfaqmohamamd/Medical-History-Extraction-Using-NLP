import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        medicines TEXT,
        directions TEXT,
        refill TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        vaccination_status TEXT,
        medical_problems TEXT,
        has_insurance TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def insert_prescription(name, address, medicines, directions, refill):
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prescriptions (name, address, medicines, directions, refill) VALUES (?, ?, ?, ?, ?)",
                   (name, address, medicines, directions, refill))
    conn.commit()
    conn.close()

def insert_patient_details(name, phone, vaccination_status, medical_problems, has_insurance):
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patient_details (name, phone, vaccination_status, medical_problems, has_insurance) VALUES (?, ?, ?, ?, ?)",
                   (name, phone, vaccination_status, medical_problems, has_insurance))
    conn.commit()
    conn.close()
