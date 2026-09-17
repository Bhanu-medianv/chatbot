from langchain_core.tools import tool


@tool
def book_appointment(
    patient_name: str,
    appointment_date: str,
    appointment_time: str,
) -> str:
    """
    Book a dental appointment.

    This tool should only be called after the patient
    has explicitly confirmed the appointment details.

    Args:
        patient_name: Full name of the patient.
        appointment_date: Requested appointment date.
        appointment_time: Requested appointment time.
    """

    print("[appointment] booking appointment")
    print(f"[appointment] patient: {patient_name}")
    print(f"[appointment] date: {appointment_date}")
    print(f"[appointment] time: {appointment_time}")

    # TODO:
    # Replace this with your actual booking API or database call.
    print('call the api for appointment')

    return (
        f"Appointment successfully booked for "
        f"{patient_name} on {appointment_date} "
        f"at {appointment_time}."
    )

