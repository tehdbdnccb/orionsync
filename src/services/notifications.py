# from src.adapters.twilio_client import send_whatsapp_message
# from src.utils.logger import log

def send_worker_update(recipient: str, message: str, media_url: str = None):
    """
    Formats and dispatches the final response back to the worker's WhatsApp.
    """
    # Formatting safety check: Ensure the message isn't empty
    if not message:
        message = "✅ Action completed successfully."

    # log.info(f"Sending notification to {recipient}")
    
    # Hand off to the adapter to actually make the HTTP request to Twilio
    # send_whatsapp_message(
    #     to=recipient,
    #     body=message,
    #     media_url=media_url
    # )
    
    # Mock output for terminal visibility during local hackathon dev
    print("\n" + "="*40)
    print(f"OUTBOUND MESSAGE TO: {recipient}")
    print("-" * 40)
    print(message)
    print("=" * 40 + "\n")