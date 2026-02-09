import requests
import json
import logging
import os
from .car_rental_bot import car_rental_bot_service

logger = logging.getLogger(__name__)

class WhatsAppResponseService:
    def __init__(self):
        self.access_token = os.environ.get('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
        self.base_url = 'https://graph.facebook.com/v18.0'
        self.enabled = bool(self.access_token and self.phone_number_id)
        
        if not self.enabled:
            logger.warning('WhatsApp Response Service not configured - missing access token or phone number ID')

    def send_text_message(self, to, message):
        """
        Send text message via WhatsApp Business API
        """
        try:
            if not self.enabled:
                logger.warning('WhatsApp Response Service not enabled')
                return {'success': False, 'error': 'Service not configured'}

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            response = requests.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                json=payload,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )

            # Raise for status to catch HTTP errors
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"WhatsApp message sent to {to}: {data}")
            
            return {
                'success': True,
                'messageId': data['messages'][0]['id'],
                'data': data
            }
        except requests.exceptions.RequestException as e:
            error_msg = e.response.json() if e.response else str(e)
            logger.error(f'Error sending WhatsApp message: {error_msg}')
            return {
                'success': False,
                'error': error_msg
            }

    def send_interactive_buttons(self, to, text, buttons, header=None, footer=None):
        """
        Send interactive buttons via WhatsApp Business API
        """
        try:
            if not self.enabled:
                logger.warning('WhatsApp Response Service not enabled')
                return {'success': False, 'error': 'Service not configured'}

            # Format buttons for WhatsApp API
            formatted_buttons = []
            for index, button in enumerate(buttons[:3]):
                formatted_buttons.append({
                    "type": "reply",
                    "reply": {
                        "id": button.get('id', f'btn_{index}'),
                        "title": button['title'][:20]
                    }
                })

            interactive_obj = {
                "type": "button",
                "body": {"text": text},
                "action": {
                    "buttons": formatted_buttons
                }
            }
            
            if header:
                interactive_obj['header'] = {"type": "text", "text": header}
            if footer:
                interactive_obj['footer'] = {"text": footer}

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "interactive",
                "interactive": interactive_obj
            }

            response = requests.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                json=payload,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )

            response.raise_for_status()
            data = response.json()
            
            logger.info(f"WhatsApp interactive buttons sent to {to}: {data}")
            
            return {
                'success': True,
                'messageId': data['messages'][0]['id'],
                'data': data
            }
        except requests.exceptions.RequestException as e:
            error_msg = e.response.json() if e.response else str(e)
            logger.error(f'Error sending WhatsApp interactive buttons: {error_msg}')
            return {
                'success': False,
                'error': error_msg
            }

    def send_interactive_list(self, to, text, button_text, sections, header=None, footer=None):
        """
        Send interactive list via WhatsApp Business API
        """
        try:
            if not self.enabled:
                logger.warning('WhatsApp Response Service not enabled')
                return {'success': False, 'error': 'Service not configured'}

            # Convert sections format if needed, but assuming calling code provides correct format
            # In JS: sections was passed directly. 
            # In Python port of Bot Logic: get_category_list_items returns a simple list of dicts.
            # We need to wrap it in a section structure for WhatsApp API if it's not already.
            
            # Check if 'sections' is just a list of items or already formatted sections
            formatted_sections = sections
            if isinstance(sections, list) and len(sections) > 0 and 'rows' not in sections[0]:
                # It's likely a simple list of items (title, description), wrap in one section
                rows = []
                for index, item in enumerate(sections):
                    row = {
                        "id": item.get('id', f"section_row_{index}"),
                        "title": item['title'][:24],
                        "description": item.get('description', '')[:72]
                    }
                    rows.append(row)
                
                formatted_sections = [{
                    "title": "Options",
                    "rows": rows
                }]

            interactive_obj = {
                "type": "list",
                "body": {"text": text},
                "action": {
                    "button": button_text,
                    "sections": formatted_sections
                }
            }

            if header:
                interactive_obj['header'] = {"type": "text", "text": header}
            if footer:
                interactive_obj['footer'] = {"text": footer}

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "interactive",
                "interactive": interactive_obj
            }

            response = requests.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                json=payload,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )

            response.raise_for_status()
            data = response.json()
            
            logger.info(f"WhatsApp interactive list sent to {to}: {data}")
            
            return {
                'success': True,
                'messageId': data['messages'][0]['id'],
                'data': data
            }
        except requests.exceptions.RequestException as e:
            error_msg = e.response.json() if e.response else str(e)
            logger.error(f'Error sending WhatsApp interactive list: {error_msg}')
            return {
                'success': False,
                'error': error_msg
            }

    def send_image_message(self, to, image_url, caption=None):
        """
        Send image message via WhatsApp Business API
        """
        try:
            if not self.enabled:
                logger.warning('WhatsApp Response Service not enabled')
                return {'success': False, 'error': 'Service not configured'}

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "image",
                "image": {
                    "link": image_url
                }
            }
            
            if caption:
                payload['image']['caption'] = caption

            response = requests.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                json=payload,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )

            response.raise_for_status()
            data = response.json()
            
            logger.info(f"WhatsApp image sent to {to}: {data}")
            
            return {
                'success': True,
                'messageId': data['messages'][0]['id'],
                'data': data
            }
        except requests.exceptions.RequestException as e:
            error_msg = e.response.json() if e.response else str(e)
            logger.error(f'Error sending WhatsApp image: {error_msg}')
            return {
                'success': False,
                'error': error_msg
            }

    def process_incoming_message(self, message_data):
        """
        Process incoming WhatsApp message with advanced car rental bot
        """
        try:
            message_from = message_data.get('from')
            message_body = message_data.get('message')
            name = message_data.get('name')
            
            logger.info(f'Processing WhatsApp message from {name} (+{message_from}): "{message_body}"')
            
            # Process through advanced car rental bot
            bot_response = car_rental_bot_service.process_message(message_from, message_body, name)
            
            if not bot_response['success']:
                logger.error(f"Bot processing failed for {name} (+{message_from}): {bot_response.get('error')}")
                return {
                    'success': False,
                    'error': bot_response.get('error')
                }

            # 1. Send Images if present
            if bot_response.get('images'):
                for img in bot_response['images']:
                    self.send_image_message(message_from, img['url'], img.get('caption'))

            # 2. Send appropriate response based on message type
            result = None
            
            if bot_response['messageType'] == 'interactive_buttons' and bot_response.get('buttons'):
                result = self.send_interactive_buttons(
                    message_from, 
                    bot_response['response'], 
                    bot_response['buttons'],
                    None,
                    'CarRental Pro - Your Premium Car Rental Service'
                )
            elif bot_response['messageType'] == 'interactive_list' and bot_response.get('listItems'):
                result = self.send_interactive_list(
                    message_from,
                    bot_response['response'],
                    'Select Option',
                    bot_response['listItems'],
                    None,
                    'CarRental Pro'
                )
            else:
                result = self.send_text_message(message_from, bot_response['response'])
            
            if result.get('success'):
                logger.info(f"Advanced response sent successfully to {name} (+{message_from})")
                
                return {
                    'success': True,
                    'message': 'Advanced car rental response sent successfully',
                    'messageId': result.get('messageId'),
                    'sessionState': bot_response.get('sessionState'),
                    'messageType': bot_response.get('messageType')
                }
            else:
                logger.error(f"Failed to send response to {name} (+{message_from}): {result.get('error')}")
                return {
                    'success': False,
                    'error': result.get('error')
                }
        except Exception as error:
            logger.error(f'Error processing incoming WhatsApp message: {error}')
            return {
                'success': False,
                'error': str(error)
            }

    def extract_message_data(self, webhook_payload):
        """
        Extract message data from WhatsApp webhook payload
        """
        try:
            entry = webhook_payload.get('entry', [])
            if entry:
                changes = entry[0].get('changes', [])
                if changes:
                    value = changes[0].get('value', {})
                    messages = value.get('messages', [])
                    if messages:
                        message = messages[0]
                        contacts = value.get('contacts', [])
                        contact = contacts[0] if contacts else None
                        
                        message_text = ''
                        message_type = message.get('type')
                        
                        # Extract message content based on type
                        if message_type == 'text':
                            message_text = message['text']['body']
                        elif message_type == 'interactive':
                            interactive = message['interactive']
                            if interactive.get('type') == 'button_reply':
                                message_text = interactive['button_reply']['title'] # We use title or ID to switch logic? JS used title in main loop, ID in button handler. Python port uses ID logic in handle_button_click but 'title' might be passed as message text.
                                # Wait, the JS `handleButtonClick` checks for ID.
                                # But `processMessage` calls `isButtonClick(message)`.
                                # The message passed to `processMessage` should be the ID if it's a button click?
                                # Let's check JS `extractMessageData`.
                                # JS: `messageText = message.interactive.button_reply.title`
                                # But `handleButtonClick` switches on `buttonId`.
                                # Wait, the JS `handleButtonClick` takes `message` as first arg.
                                # And `isButtonClick` checks `message` against patterns (titles) OR IDs (starts with 'car_').
                                # The Python port checks `is_button_click(message)`.
                                # If I pass title, it matches 'Browse Cars'.
                                # If I pass ID, it matches 'browse_cars'.
                                # I should probably pass the ID if available?
                                # The JS code extracts TITLE: `messageText = message.interactive.button_reply.title`.
                                # AND checks if title is in `buttonPatterns`.
                                # BUT for dynamic buttons (car_123), the TITLE is "1. Toyota". That does NOT start with `car_`.
                                # So there is a discrepancy in the JS logic or my understanding.
                                # JS: `buttonPatterns` includes titles like '🚗 Browse Cars'.
                                # BUT `car_` logic?
                                # Ah, `formattedButtons` in JS sets ID: `button.id || btn_${index}`.
                                # When a button is clicked, we get ID and TITLE.
                                # JS `extractMessageData`: `messageText = message.interactive.button_reply.title`.
                                # So it passes the TITLE to `processMessage`.
                                # Then `isButtonClick` checks if TITLE matches.
                                # BUT: `message.startsWith('car_')`?
                                # If title is "1. Toyota Vitz", it does NOT start with "car_".
                                # So the JS code might be slightly buggy or expects ID to be passed?
                                # Let's look again at JS `extractMessageData`.
                                # It explicitly extracts title.
                                # Wait, for `button_reply`, it has `id` and `title`.
                                # The standard webhook payload has `button_reply: { id: "...", title: "..." }`.
                                # If I want to support IDs (which are robust), I should extract ID.
                                # BUT the JS code extracts TITLE.
                                # Let's FIX this in Python to be better. I will prioritize ID if available.
                                message_text = interactive['button_reply']['id']
                            elif interactive.get('type') == 'list_reply':
                                message_text = interactive['list_reply']['id'] # Use ID for robustness
                                # JS used title. I'll use ID because my Python logic expects IDs for `car_` etc.
                        else:
                            message_text = f"[{message_type} message]"
                        
                        return {
                            'from': message['from'],
                            'message': message_text,
                            'messageId': message['id'],
                            'timestamp': message['timestamp'],
                            'name': contact['profile']['name'] if contact else 'Customer',
                            'messageType': message_type
                        }
            return None
        except Exception as error:
            logger.error(f'Error extracting message data: {error}')
            return None

whatsapp_service = WhatsAppResponseService()
