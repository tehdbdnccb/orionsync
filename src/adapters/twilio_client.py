import httpx
from twilio.rest import Client
from config.settings import get_settings

settings = get_settings()
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

def send_whatsapp_message(to: str, body: str, media_url: str = None):
    """
    Pushes a WhatsApp message back to the deskless worker.
    """
    params = {
        "from_": f"whatsapp:{settings.twilio_phone_number}",
        "to": to,
        "body": body
    }
    if media_url:
        params["media_url"] = [media_url]

    message = twilio_client.messages.create(**params)
    return message.sid

def download_twilio_media(media_url: str, save_path: str) -> str:
    """
    Downloads inbound voice notes or images from Twilio securely.
    """
    # Twilio requires Basic Auth to fetch media URLs
    auth = (settings.twilio_account_sid, settings.twilio_auth_token)
    
    with httpx.Client() as client:
        response = client.get(media_url, auth=auth, follow_redirects=True)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
            
    return save_path