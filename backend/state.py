# backend/state.py
from typing import TypedDict, Optional, List, Dict

class MedicalState(TypedDict):
    raw_input: str

    summary: Optional[str]
    severity: Optional[str]          # normal | mild | critical
    department: Optional[str]
    disease_type: Optional[str]
    location: Optional[str]

    doctors: Optional[List[Dict]]
    user_confirmation: Optional[str]
    selected_doctor: Optional[Dict]

    patient_name: Optional[str]
    patient_email: Optional[str]
    preferred_date: Optional[str]
    preferred_time: Optional[str]

    appointment: Optional[Dict]
    end: bool
