# backend/input_handlers/dispatcher.py
from .text import handle_text
from .pdf import handle_pdf
from .image import handle_image

def handle_input(input_type: str, payload):
    if input_type == "text":
        return handle_text(payload)
    elif input_type == "pdf":
        return handle_pdf(payload)
    elif input_type == "image":
        return handle_image(payload)
    else:
        raise ValueError("Unsupported input type")
