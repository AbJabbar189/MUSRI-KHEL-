import sqlite3

def update_db():
    conn = sqlite3.connect('misri_khel.db')
    cursor = conn.cursor()

    # Get central committee id
    cursor.execute("SELECT id FROM committees WHERE committee_type = 'CENTRAL' LIMIT 1")
    row = cursor.fetchone()
    if row:
        central_id = row[0]
    else:
        cursor.execute("INSERT INTO committees (name_ur, name_en, committee_type, description, is_active) VALUES (?, ?, ?, ?, 1)",
                       ("مرکزی کابینہ", "Central Cabinet", "CENTRAL", "مرکزی سپریم کونسل و کابینہ"))
        central_id = cursor.lastrowid

    # Clear old office bearers of central
    cursor.execute("DELETE FROM office_bearers WHERE committee_id = ?", (central_id,))

    cabinet = [
        ("سرپرست اعلیٰ", "Chief Patron", "عبد اللہ بھائی", "Abdullah Bhai"),
        ("وائس چیئرمین", "Vice Chairman", "محمد ذوالقرنین", "Muhammad Zulqarnain"),
        ("ڈپٹی چیئرمین", "Deputy Chairman", "صلاح الدین ایوبی", "Salahuddin Ayubi"),
        ("صدر", "President", "نصیب زمین بھائی", "Naseeb Zameen Bhai"),
        ("نائب صدر", "Vice President", "نظیر محمد بھائی", "Nazir Muhammad Bhai"),
        ("سینئر نائب صدر", "Senior Vice President", "محمد نواب بھائی", "Muhammad Nawab Bhai"),
        ("جوئنیر نائب صدر", "Junior Vice President", "مولانا محمد سلیمان بھائی", "Maulana Muhammad Sulaiman Bhai"),
        ("جنرل سیکرٹری", "General Secretary", "فرید الرحمٰن", "Farid-ur-Rehman"),
        ("نائب ڈپٹی جنرل سیکرٹری", "Naib Deputy General Secretary", "فخر البشر صاحب", "Fakhr-ul-Bashar Sahib"),
        ("جوائنٹ سیکرٹری", "Joint Secretary", "تاج معین اللہ بھائی", "Taj Moeenullah Bhai"),
        ("خزانچی", "Treasurer", "مولانا مطیع اللہ صاحب", "Maulana Mutee-ullah Sahib"),
        ("سیکرٹری تنظیم", "Organizing Secretary", "محمد زمان درویش", "Muhammad Zaman Darwesh"),
        ("سیکرٹری تعلیم", "Education Secretary", "حیات گل بھائی", "Hayat Gul Bhai"),
        ("سیکرٹری فلاحی امور", "Welfare Secretary", "نور قیوم بھائی", "Noor Qayyum Bhai"),
        ("آفس سیکرٹری", "Office Secretary", "عبد القوی بھائی", "Abdul Qawi Bhai")
    ]

    for title_ur, title_en, name_ur, name_en in cabinet:
        cursor.execute("""
            INSERT INTO office_bearers (committee_id, title_ur, title_en, name_ur, name_en, is_public, is_active)
            VALUES (?, ?, ?, ?, ?, 1, 1)
        """, (central_id, title_ur, title_en, name_ur, name_en))

    conn.commit()
    conn.close()
    print("Database updated with official Central Cabinet members successfully!")

if __name__ == "__main__":
    update_db()
