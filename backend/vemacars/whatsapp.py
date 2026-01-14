import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_whatsapp_message(to_number, message):
    """
    to_number: customer number (e.g. 255...)
    message: text content
    """
    # Clean the phone number (ensure no + or spaces)
    clean_number = "".join(filter(str.isdigit, str(to_number)))

    payload = {
        'device': settings.WAPBRIDGE_DEVICE_ID, # Most bridges use a Device ID
        'to': clean_number,
        'message': message
    }
    
    headers = {
        'Authorization': f'Bearer {settings.WAPBRIDGE_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{settings.WAPBRIDGE_BASE_URL}/send", 
            json=payload, 
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"WhatsApp API Error: {e}")
        return {"status": "error", "message": str(e)}