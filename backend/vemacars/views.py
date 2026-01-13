from django.http import JsonResponse
from .whatsapp import send_whatsapp_message
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def whatsapp_webhook(request):
    data = json.loads(request.body)

    text = data.get("message", "").lower()
    sender = data.get("from")

    if "booking" in text:
        reply = "🚗 To book a car, visit vemacars.com"
    elif "hello" in text:
        reply = "Hello 👋 How can I help you?"
    else:
        reply = "Sorry, I didn’t understand that."

    send_whatsapp_message(
        from_number="255789478202",  # your WhatsApp line
        to_number=sender,            # customer number
        message=reply
    )

    return JsonResponse({"status": "ok"})


@csrf_exempt
def send_message_from_frontend(request):
    data = json.loads(request.body)

    phone = data.get("phone")
    message = data.get("message")

    if not phone or not message:
        return JsonResponse({"error": "Missing data"}, status=400)

    result = send_whatsapp_message(
        from_number="255789478202",
        to_number=phone,
        message=message
    )

    return JsonResponse({"status": "sent", "result": result})

    
# def test_whatsapp(request):
#     result = send_whatsapp_message(
#         from_number = '+255789478202',
#         to_number = '+255789478202',
#         message = 'Hello from Mariam!'
#     )
    
#     return JsonResponse(result)
    
    
