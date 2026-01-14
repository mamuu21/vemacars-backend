from django.http import JsonResponse, HttpResponse
from .whatsapp import send_whatsapp_message
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def whatsapp_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body)
        
        # 1. Prevent loop: Check if this is an INCOMING message
        # Wapbridge usually sends 'event': 'message_received' or similar
        if data.get("event") != "message.received":
            return JsonResponse({"status": "ignored_event"})

        msg_obj = data.get("data", {})
        text = msg_obj.get("body", "").lower()
        sender = msg_obj.get("from") # Format usually '255xxx@c.us'
        
        # Clean the sender string to just numbers
        sender_phone = sender.split('@')[0] if sender else None

        if not sender_phone or not text:
            return JsonResponse({"status": "invalid_data"})

        # 2. Basic Bot Logic
        if "booking" in text:
            reply = "🚗 To book a car, visit vemacars.com"
        elif "hello" in text or "hi" in text:
            reply = "Hello 👋 Welcome to Vema Cars. How can I help you today?"
        else:
            return JsonResponse({"status": "no_reply_needed"})

        # 3. Send the reply
        send_whatsapp_message(to_number=sender_phone, message=reply)

    except Exception as e:
        print(f"Webhook Error: {e}")
        
    return JsonResponse({"status": "ok"})

@csrf_exempt
def send_message_from_frontend(request):
    """
    Action: User clicks 'Book' or 'Contact' on Next.js
    """
    if request.method == "POST":
        data = json.loads(request.body)
        phone = data.get("phone")
        message = data.get("message", "Hello, I am interested in a car rental.")

        if not phone:
            return JsonResponse({"error": "Phone number is required"}, status=400)

        result = send_whatsapp_message(to_number=phone, message=message)
        return JsonResponse({"status": "processed", "api_response": result})
    
    return HttpResponse(status=405)