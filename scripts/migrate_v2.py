import sqlite3
import os

db_path = 'misri_khel.db'
if not os.path.exists(db_path):
    print("DB not found at root, checking backend...")
    db_path = 'backend/misri_khel.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

def add_col_if_not_exists(table, col, col_type):
    c.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in c.fetchall()]
    if col not in cols:
        print(f"Adding {col} to {table}...")
        c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")

# Add new columns to membership_applications
add_col_if_not_exists('membership_applications', 'cnic', 'VARCHAR(25)')
add_col_if_not_exists('membership_applications', 'entry_fee', 'FLOAT DEFAULT 300.0')
add_col_if_not_exists('membership_applications', 'fee_status', "VARCHAR(50) DEFAULT 'PAID'")
add_col_if_not_exists('membership_applications', 'payment_method', "VARCHAR(50) DEFAULT 'EasyPaisa'")
add_col_if_not_exists('membership_applications', 'transaction_reference', 'VARCHAR(100)')
add_col_if_not_exists('membership_applications', 'receipt_slip_path', 'VARCHAR(255)')

# Add new columns to members
add_col_if_not_exists('members', 'cnic', 'VARCHAR(25)')
add_col_if_not_exists('members', 'entry_fee', 'FLOAT DEFAULT 300.0')
add_col_if_not_exists('members', 'fee_status', "VARCHAR(50) DEFAULT 'PAID'")
add_col_if_not_exists('members', 'payment_method', "VARCHAR(50) DEFAULT 'EasyPaisa'")
add_col_if_not_exists('members', 'transaction_reference', 'VARCHAR(100)')
add_col_if_not_exists('members', 'receipt_slip_path', 'VARCHAR(255)')

# Update sample member record with real test data
c.execute("""
    UPDATE members 
    SET cnic = '15201-1234567-1',
        entry_fee = 300.0,
        fee_status = 'PAID',
        payment_method = 'EasyPaisa',
        transaction_reference = 'EP-982341890',
        receipt_slip_path = 'images/sample_receipt.jpg'
    WHERE id = 1
""")

c.execute("""
    UPDATE membership_applications 
    SET cnic = '15201-1234567-1',
        entry_fee = 300.0,
        fee_status = 'PAID',
        payment_method = 'EasyPaisa',
        transaction_reference = 'EP-982341890',
        receipt_slip_path = 'images/sample_receipt.jpg'
    WHERE id = 1
""")

conn.commit()
conn.close()
print("Migration completed successfully!")
