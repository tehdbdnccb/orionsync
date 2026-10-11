from src.adapters.twilio_client import send_whatsapp_message


def send_worker_update(recipient: str, message: str, media_url: str = None):
    """
    Formats and dispatches the final response back to the worker's WhatsApp.
    """
    # Formatting safety check: Ensure the message isn't empty
    if not message:
        message = "✅ Action completed successfully."

    send_whatsapp_message(to=recipient, body=message, media_url=media_url)

