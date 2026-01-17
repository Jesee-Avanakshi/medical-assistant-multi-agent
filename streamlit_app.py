import streamlit as st
from backend.input_handlers.dispatcher import handle_input
from backend.graph import app as graph_app
from backend.agents.booking import book_appointment
from backend.agents.emailer import send_email
from datetime import datetime

st.set_page_config(
    page_title="Medical Assistant",
    layout="wide"
)

st.title("🩺 Medical Assistant")
st.caption("AI-powered medical report understanding & appointment booking")

# ---------------------------------------------
# Input section
# ----------------------------------------------
input_type = st.radio(
    "Choose input type",
    ["Text", "PDF", "Image"],
    horizontal=True
)

raw_text = None
uploaded_file = None

if input_type == "Text":
    raw_text = st.text_area(
        "Enter medical notes",
        height=150,
        placeholder="Paste doctor notes or patient symptoms..."
    )
else:
    uploaded_file = st.file_uploader(
        f"Upload {input_type} file",
        type=["pdf", "png", "jpg", "jpeg"]
    )

# ---------------------------------------------
# Sidebar
# ----------------------------------------------
with st.sidebar:
    st.warning("⚠️ This system does not provide medical diagnosis.")
    st.write (""" It only:\n
    Assists in understanding reports \n
    Helps with doctor consultation
""")


if st.button("Analyze Report"):
    if input_type == "Text" and not raw_text:
        st.warning("Please enter medical text.")
        st.stop()

    if input_type != "Text" and not uploaded_file:
        st.warning("Please upload a file.")
        st.stop()

    # Convert input → text
    if input_type == "Text":
        extracted_text = raw_text
    else:
        file_path = f"/tmp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        extracted_text = handle_input(input_type.lower(), file_path)

    initial_state = {
        "raw_input": extracted_text,
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

    st.session_state["state"] = graph_app.invoke(initial_state)

state = st.session_state.get("state")

if not state:
    st.stop()

if state:
    st.subheader("🧾 Report Summary")
    st.write(state["summary"])

    st.subheader("⚠️ Severity")
    st.write(state["severity"].upper())

    if state["severity"] == "normal":
        st.success("✅ No critical issues detected. Please follow routine care.")
        st.stop()

if state.get("severity") and state["severity"] in ["mild", "critical"]:
    st.subheader("👨‍⚕️ Recommended Doctors")

    for idx, doc in enumerate(state["doctors"]):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(
                f"**{doc['name']}**  \n"
                f"{doc['hospital']}  \n"
                f"{doc['experience']} years experience"
            )
        with col2:
            if st.button("Book", key=f"book_{idx}"):
                st.session_state["selected_doctor"] = doc


if "selected_doctor" in st.session_state:
    st.subheader("📅 Book Appointment")

    name = st.text_input("Patient Name")
    email = st.text_input("Patient Email")
    date = st.date_input("Preferred Date")
    time = st.time_input("Preferred Time")

    
    if st.button("Confirm Appointment"):
        # Optional UI guard
        selected_dt = datetime.combine(date, time)
        if selected_dt <= datetime.now():
            st.warning("Please select a future date & time.")
            st.stop()
        state.update({
            "selected_doctor": st.session_state["selected_doctor"],
            "patient_name": name,
            "patient_email": email,
            "preferred_date": str(date),
            "preferred_time": time.strftime("%H:%M")
        })

        state = book_appointment(state)

        if state.get("error"):
            st.error(state["error"])
            st.stop()

        # ✅ Send email (plain Python)
        state = send_email(state)

        st.success("✅ Appointment booked successfully!")
