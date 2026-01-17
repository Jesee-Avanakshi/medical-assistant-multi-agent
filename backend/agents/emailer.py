from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from backend.state import MedicalState

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def send_email(state: MedicalState) -> MedicalState:
    appointment = state.get("appointment")

    if not appointment:
        print("⚠️ No appointment found. Skipping email.")
        state["end"] = True
        return state

    sg = SendGridAPIClient(SENDGRID_API_KEY)

    # ---------------- Patient Email ----------------
    patient_msg = Mail(
        from_email=SENDER_EMAIL,
        to_emails=appointment["patient_email"],
        subject="Appointment Confirmation",
        html_content=f"""
        <h3>Your Appointment is Confirmed</h3>
        <p><b>Appointment ID:</b> {appointment["appointment_id"]}</p>
        <p><b>Doctor:</b> {appointment["doctor"]["name"]}</p>
        <p><b>Hospital:</b> {appointment["doctor"]["hospital"]}</p>
        <p><b>Date & Time:</b> {appointment["datetime"]}</p>
        """
    )

    # ---------------- Doctor Email ----------------
    doctor_msg = Mail(
        from_email=SENDER_EMAIL,
        to_emails=appointment["doctor"]["email"],
        subject="New Patient Appointment",
        html_content=f"""
        <h3>New Appointment Booked</h3>
        <p><b>Appointment ID:</b> {appointment["appointment_id"]}</p>
        <p><b>Patient Name:</b> {appointment["patient_name"]}</p>
        <p><b>Date & Time:</b> {appointment["datetime"]}</p>
        """
    )

    try:
        sg.send(patient_msg)
        sg.send(doctor_msg)
        print("📧 Emails sent successfully via SendGrid")
    except Exception as e:
        print("⚠️ Email sending failed:", str(e))

    state["end"] = True
    return state
