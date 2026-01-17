import sqlite3
from backend.state import MedicalState

DB_PATH = "backend/db/doctors.db"

def recommend_doctors(state: MedicalState) -> MedicalState:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, specialization, hospital, experience, email
        FROM doctors
        WHERE specialization = ? AND city = ?
        ORDER BY experience DESC
    """, (state["department"].lower(), state["location"]))

    rows = cursor.fetchall()
    conn.close()

    state["doctors"] = [
        {
            "name": r[0],
            "specialization": r[1],
            "hospital": r[2],
            "experience": r[3],
            "email": r[4]
        }
        for r in rows
    ]
    return state
