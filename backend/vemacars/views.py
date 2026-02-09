from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.conf import settings
from .whatsapp_cloud import whatsapp_service

logger = logging.getLogger(__name__)

@csrf_exempt
def whatsapp_webhook(request):
    # 1. Verification Challenge (GET)
    if request.method == "GET":
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        # You should define WHATSAPP_VERIFY_TOKEN in env/settings. 
        # For now, I'll default to a simple check or 'vemacars_verify_token'
        verify_token = getattr(settings, 'WHATSAPP_VERIFY_TOKEN', 'vemacars_secret')

        if mode == 'subscribe' and token == verify_token:
            logger.info("Webhook verified successfully")
            return HttpResponse(challenge, status=200)
        else:
            logger.warning(f"Webhook Verification Failed. Received: {token}, Expected: {verify_token}")
            return HttpResponse('Forbidden', status=403)

    # 2. Event Notifications (POST)
    if request.method == "POST":
        try:
            # Enhanced Logging for Debugging
            body_unicode = request.body.decode('utf-8')
            logger.info(f"Received Webhook Payload: {body_unicode}")
            
            data = json.loads(body_unicode)
            
            # Extract basic info first
            entry = data.get('entry', [])
            if not entry:
                logger.warning("Ignored webhook: No 'entry' field found.")
                return JsonResponse({"status": "ignored_bad_format"})
            
            # Use the service to extract standardized message data
            message_data = whatsapp_service.extract_message_data(data)
            
            if message_data:
                # Direct synchronous call since we removed async from service
                result = whatsapp_service.process_incoming_message(message_data)
                
                if result.get('success'):
                    return JsonResponse({"status": "processed"})
                else:
                    logger.error(f"Processing failed: {result.get('error')}")
                    return JsonResponse({"status": "error", "error": result.get('error')}, status=500)
            
            logger.info("Ignored webhook: No valid message data extracted.")
            return JsonResponse({"status": "ignored_no_message"})
            
            return JsonResponse({"status": "ignored_no_message"})

        except Exception as e:
            logger.error(f"Webhook Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return HttpResponse(status=405)

@csrf_exempt
def send_message_from_frontend(request):
    """
    Action: User clicks 'Book' or 'Contact' on Next.js
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get("phone")
            message = data.get("message", "Hello, I am interested in a car rental.")

            if not phone:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            # Use new service
            result = whatsapp_service.send_text_message(to=phone, message=message)
            
            if result['success']:
                return JsonResponse({"status": "processed", "api_response": result['data']})
            else:
                 return JsonResponse({"status": "error", "error": result['error']}, status=500)

        except Exception as e:
             return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return HttpResponse(status=405)