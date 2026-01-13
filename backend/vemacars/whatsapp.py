import requests
from django.conf import settings


def send_whatsapp_message(from_number, to_number, message):
    payload= {
        'from_number': from_number,
        'to_number': to_number,
        'message': message
    }
    
    headers = {
        'Authorization': settings.WAPBRIDGE_TOKEN
    }
    
    response = requests.post(settings.WAPBRIDGE_BASE_URL, json=payload, headers=headers)
    return response.json()