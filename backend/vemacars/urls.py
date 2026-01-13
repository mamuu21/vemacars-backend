from django.urls import path
from .views import whatsapp_webhook, send_message_from_frontend



urlpatterns = [
    # path("test-whatsapp/", test_whatsapp, name="test_whatsapp"),
    path("webhooks/whatsapp/", whatsapp_webhook),
    path("api/send-whatsapp/", send_message_from_frontend),

]
