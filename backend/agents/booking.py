from datetime import datetime
import uuid
from backend.state import MedicalState

def book_appointment(state: MedicalState) -> MedicalState:
    dt = datetime.strptime(
        f"{state['preferred_date']} {state['preferred_time']}",
        "%Y-%m-%d %H:%M"
    )

    if dt <= datetime.now():
        raise ValueError("Appointment must be in the future")

    state["appointment"] = {
        "appointment_id": f"APT-{uuid.uuid4().hex[:6]}",
        "doctor": state["selected_doctor"],
        "patient_name": state["patient_name"],
        "patient_email": state["patient_email"],
        "datetime": dt.isoformat()
    }
    return state
