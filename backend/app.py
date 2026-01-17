# backend/app.py

from backend.graph import app

# ---- Sanity Test Input ----
state = {
    "raw_input": "Patient reports chest pain, shortness of breath, and irregular heartbeat.",
    "summary": None,
    "severity": None,
    "department": None,
    "disease_type": None,
    "location": None,
    "doctors": None,
    "selected_doctor": None,
    "patient_name": None,
    "patient_email": None,
    "preferred_date": None,
    "preferred_time": None,
    "user_confirmation": None,
    "appointment": None,
    "end": False
}

# ---- Run graph until recommendation ----
result = app.invoke(state)

print("\n=== SANITY CHECK OUTPUT ===")
print("Severity:", result["severity"])
print("Department:", result["department"])
print("Doctors Found:", len(result.get("doctors", [])))
print("===========================\n")



# from backend.graph import app

# initial_state = {
#     "raw_input": "",
#     "summary": None,
#     "severity": None,
#     "department": None,
#     "disease_type": None,
#     "location": None,
#     "doctors": None,
#     "selected_doctor": None,
#     "patient_name": None,
#     "patient_email": None,
#     "preferred_date": None,
#     "preferred_time": None,
#     "user_confirmation": None,
#     "appointment": None,
#     "end": False
# }

# result = app.invoke(initial_state)
# print(result)
