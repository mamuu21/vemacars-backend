import logging
import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class CarRentalBotService:
    def __init__(self):
        self.cars = self.initialize_car_catalog()
        self.bookings: Dict[str, Any] = {} # In-memory storage for demo
        self.customer_sessions: Dict[str, Any] = {} # Track customer conversation state

    def initialize_car_catalog(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Initialize car catalog with real data
        """
        base_url = "https://peskier-unslaked-ken.ngrok-free.dev" # Using the configured Ngrok domain
        
        return {
            'economy': [
                {
                    'id': 'eco_001',
                    'name': 'Toyota Vitz',
                    'price': 2500,
                    'features': ['Automatic', 'AC', 'Fuel Efficient', '4 Seats'],
                    'image': f'{base_url}/media/cars/subaru.jpg', # Using placeholder subaru for small car
                    'available': True,
                    'location': 'Nairobi, Dar es Salaam'
                },
                {
                    'id': 'eco_002',
                    'name': 'Nissan March',
                    'price': 2800,
                    'features': ['Manual/Auto', 'AC', 'Bluetooth', '4 Seats'],
                    'image': f'{base_url}/media/cars/subaru.jpg',
                    'available': True,
                    'location': 'Nairobi, Mombasa'
                },
                {
                    'id': 'eco_003',
                    'name': 'Suzuki Swift',
                    'price': 3000,
                    'features': ['Automatic', 'AC', 'Sport Mode', '4 Seats'],
                    'image': f'{base_url}/media/cars/subaru.jpg',
                    'available': False,
                    'location': 'Nairobi'
                }
            ],
            'suv': [
                {
                    'id': 'suv_001',
                    'name': 'Toyota RAV4',
                    'price': 4500,
                    'features': ['AWD', 'Automatic', 'AC', '7 Seats', 'GPS'],
                    'image': f'{base_url}/media/cars/rav4.jpg',
                    'available': True,
                    'location': 'Nairobi, Dar es Salaam, Mombasa'
                },
                {
                    'id': 'suv_002',
                    'name': 'Honda CR-V',
                    'price': 5000,
                    'features': ['AWD', 'Automatic', 'Sunroof', '5 Seats', 'Premium Sound'],
                    'image': f'{base_url}/media/cars/rav4.jpg',
                    'available': True,
                    'location': 'Nairobi, Kampala'
                },
                {
                    'id': 'suv_003',
                    'name': 'Mazda CX-5',
                    'price': 5500,
                    'features': ['AWD', 'Automatic', 'Leather', '5 Seats', 'Premium Interior'],
                    'image': f'{base_url}/media/cars/rav4.jpg',
                    'available': True,
                    'location': 'Nairobi'
                }
            ],
            'luxury': [
                {
                    'id': 'lux_001',
                    'name': 'Mercedes C-Class',
                    'price': 8000,
                    'features': ['Automatic', 'Leather', 'Premium Sound', '5 Seats', 'GPS', 'Sunroof'],
                    'image': f'{base_url}/media/cars/alphard.webp', # Placeholder
                    'available': True,
                    'location': 'Nairobi, Dar es Salaam'
                },
                {
                    'id': 'lux_002',
                    'name': 'BMW 3 Series',
                    'price': 9000,
                    'features': ['Automatic', 'Sport Mode', 'Premium Interior', '5 Seats', 'iDrive'],
                    'image': f'{base_url}/media/cars/alphard.webp',
                    'available': True,
                    'location': 'Nairobi'
                },
                {
                    'id': 'lux_003',
                    'name': 'Audi A4',
                    'price': 10000,
                    'features': ['Quattro AWD', 'Automatic', 'Virtual Cockpit', '5 Seats', 'Premium Plus'],
                    'image': f'{base_url}/media/cars/alphard.webp',
                    'available': False,
                    'location': 'Nairobi, Kampala'
                }
            ],
            'van': [
                {
                    'id': 'van_001',
                    'name': 'Toyota Alphard', # Renamed to match image
                    'price': 6000,
                    'features': ['Manual', 'AC', '14 Seats', 'Luggage Space'],
                    'image': f'{base_url}/media/cars/alphard.webp',
                    'available': True,
                    'location': 'Nairobi, Dar es Salaam, Mombasa'
                },
                {
                    'id': 'van_002',
                    'name': 'Nissan Caravan',
                    'price': 7000,
                    'features': ['Automatic', 'AC', '12 Seats', 'Premium Interior'],
                    'image': f'{base_url}/media/cars/alphard.webp',
                    'available': True,
                    'location': 'Nairobi, Kampala'
                }
            ]
        }

    def process_message(self, phone_number: str, message: str, customer_name: str = 'Customer') -> Dict[str, Any]:
        """
        Process customer message with advanced bot intelligence
        """
        try:
            logger.info(f'Processing message from {customer_name} (+{phone_number}): "{message}"')

            # Get or create customer session
            session = self.get_customer_session(phone_number)
            lower_message = message.lower()

            # Update session with current message
            session['lastMessage'] = message
            session['messageCount'] += 1

            # Determine intent and generate response
            response = ""
            message_type = 'text'
            buttons = None
            list_items = None
            images = []

            # Handle button clicks and interactive responses
            if self.is_button_click(message):
                return self.handle_button_click(message, session, customer_name, phone_number)

            # Greeting and welcome
            if self.is_greeting(lower_message):
                response = self.generate_welcome_message(customer_name)
                buttons = self.get_main_menu_buttons()
                message_type = 'interactive_buttons'
                session['state'] = 'main_menu'
            
            # Car catalog requests
            elif self.is_car_catalog_request(lower_message):
                category = self.extract_car_category(lower_message)
                if category:
                    response = self.generate_car_catalog(category, customer_name)
                    buttons = self.get_car_category_buttons(category)
                    
                    # Extract images for the cars in this category
                    cars = self.cars.get(category, [])[:3] # Limit to top 3
                    images = [
                        {'url': c['image'], 'caption': f"{c['name']} - TZS {c['price']:,}/day"} 
                        for c in cars if c.get('image')
                    ]
                    
                    message_type = 'interactive_buttons'
                    session['state'] = 'browsing_cars'
                    session['selectedCategory'] = category
                else:
                    response = self.generate_category_selection(customer_name)
                    list_items = self.get_category_list_items()
                    message_type = 'interactive_list'
                    session['state'] = 'selecting_category'
            
            # Specific car selection
            elif self.is_car_selection(lower_message):
                car_id = self.extract_car_id(lower_message, session.get('selectedCategory'))
                if car_id:
                    car = self.get_car_by_id(car_id)
                    response = self.generate_car_details(car, customer_name)
                    buttons = self.get_car_action_buttons(car_id)
                    
                    # Add image for the selected car
                    if car.get('image'):
                        images = [{'url': car['image'], 'caption': car['name']}]
                    else:
                        images = []

                    message_type = 'interactive_buttons'
                    session['state'] = 'viewing_car'
                    session['selectedCar'] = car_id
                else:
                     response = self.generate_car_not_found(customer_name)

            # Booking requests
            elif self.is_booking_request(lower_message):
                if session.get('selectedCar'):
                    response = self.generate_booking_form(session['selectedCar'], customer_name)
                    buttons = self.get_booking_form_buttons()
                    message_type = 'interactive_buttons'
                    session['state'] = 'booking_form'
                else:
                    response = self.generate_select_car_first(customer_name)
                    buttons = self.get_main_menu_buttons()
                    message_type = 'interactive_buttons'

            # Booking form processing
            elif session.get('state') == 'booking_form' and self.is_booking_details(lower_message):
                booking_details = self.extract_booking_details(message)
                if booking_details['isValid']:
                    booking = self.create_booking(phone_number, session['selectedCar'], booking_details, customer_name)
                    response = self.generate_booking_confirmation(booking, customer_name)
                    buttons = self.get_payment_buttons(booking['id'])
                    message_type = 'interactive_buttons'
                    session['state'] = 'payment_pending'
                    session['currentBooking'] = booking['id']
                else:
                    response = self.generate_booking_form_error(booking_details['errors'], customer_name)
                    buttons = self.get_booking_form_buttons()
                    message_type = 'interactive_buttons'

            # Payment processing
            elif session.get('state') == 'payment_pending' and self.is_payment_request(lower_message):
                booking = self.bookings.get(session.get('currentBooking'))
                if booking:
                    response = self.generate_payment_instructions(booking, customer_name)
                    buttons = self.get_payment_confirmation_buttons(booking['id'])
                    message_type = 'interactive_buttons'
                    session['state'] = 'payment_instructions'

            # Payment confirmation
            elif session.get('state') == 'payment_instructions' and self.is_payment_confirmation(lower_message):
                booking = self.bookings.get(session.get('currentBooking'))
                if booking:
                    response = self.generate_payment_success(booking, customer_name)
                    buttons = self.get_post_payment_buttons()
                    message_type = 'interactive_buttons'
                    session['state'] = 'booking_complete'
                    # Update booking status
                    booking['status'] = 'paid'
                    booking['paymentDate'] = datetime.datetime.now().isoformat()

            # Price inquiries
            elif self.is_price_inquiry(lower_message):
                response = self.generate_pricing_info(customer_name)
                buttons = self.get_category_buttons()
                message_type = 'interactive_buttons'

            # Location and availability
            elif self.is_location_inquiry(lower_message):
                response = self.generate_location_info(customer_name)
                buttons = self.get_main_menu_buttons()
                message_type = 'interactive_buttons'

            # Help and support
            elif self.is_help_request(lower_message):
                response = self.generate_help_message(customer_name)
                buttons = self.get_help_buttons()
                message_type = 'interactive_buttons'

            # Check existing bookings
            elif self.is_booking_check(lower_message):
                customer_bookings = self.get_customer_bookings(phone_number)
                response = self.generate_booking_status(customer_bookings, customer_name)
                if len(customer_bookings) > 0:
                    buttons = self.get_booking_management_buttons()
                    message_type = 'interactive_buttons'
                else:
                    buttons = self.get_main_menu_buttons()
                    message_type = 'interactive_buttons'

            # Default response with smart suggestions
            else:
                response = self.generate_smart_response(message, session, customer_name)
                buttons = self.get_contextual_buttons(session)
                message_type = 'interactive_buttons'
            
            # Update session
            self.update_customer_session(phone_number, session)

            # Note: handle_button_click returns early, so we don't reach here if it was a button click
            if images is None: images = [] # Initialize if not set in flow above
            
            return {
                'success': True,
                'response': response,
                'messageType': message_type,
                'buttons': buttons,
                'listItems': list_items,
                'customerName': customer_name,
                'phoneNumber': phone_number,
                'sessionState': session.get('state'),
                'images': images
            }

        except Exception as error:
            logger.error(f'Error processing car rental message: {error}')
            return {
                'success': False,
                'error': str(error),
                'response': f'Sorry {customer_name}, I encountered an error. Please try again or contact support.'
            }

    def generate_welcome_message(self, customer_name):
        return (
            f"👋 Hello {customer_name}! Welcome to CarRental Pro!\n\n"
            f"🚗 Your Premium Car Rental Service\n\n"
            f"I'm your personal car rental assistant. I can help you:\n\n"
            f"🔍 Browse Our Fleet\n"
            f"• SUVs from TZS 45,000/day\n"
            f"• Luxury cars from TZS 80,000/day\n"
            f"• Vans from TZS 60,000/day\n\n"
            f"📅 Quick Services\n"
            f"• Instant availability check\n"
            f"• Real-time booking\n"
            f"• Price comparisons\n"
            f"• Location-based search\n\n"
            f"💎 Premium Features\n"
            f"• 24/7 support\n"
            f"• Free delivery\n"
            f"• Comprehensive insurance\n"
            f"• Flexible payment options\n\n"
            f"What would you like to do today?"
        )

    def generate_car_catalog(self, category, customer_name):
        cars = self.cars.get(category, [])
        category_name = category.capitalize()
        
        catalog = f"🚗 {category_name} Cars Available for {customer_name}\n\n"
        
        for index, car in enumerate(cars):
            status = '✅ Available' if car['available'] else '❌ Unavailable'
            features = ' • '.join(car['features'][:3])
            
            catalog += (
                f"{index + 1}. {car['name']} {status}\n"
                f"💰 TZS {car['price']:,}/day\n"
                f"⭐ {features}\n"
                f"📍 {car['location']}\n\n"
            )

        catalog += (
            f"💡 Tip: Reply with the car number (e.g., \"1\" for {cars[0]['name'] if cars else 'First Car'}) to see full details and book!\n\n"
            f"🔄 Need something else? Try:\n"
            f"• \"Show luxury cars\"\n"
            f"• \"Compare prices\"\n"
            f"• \"Check availability\""
        )

        return catalog

    def generate_car_details(self, car, customer_name):
        if not car:
            return f"Sorry {customer_name}, car not found."

        status = '✅ Available Now' if car['available'] else '❌ Currently Unavailable'
        features = '\n• '.join(car['features'])

        return (
            f"🚗 {car['name']} - Detailed Information\n\n"
            f"{status}\n"
            f"💰 Price: TZS {car['price']:,}/day\n"
            f"📍 Locations: {car['location']}\n\n"
            f"⭐ Features:\n"
            f"• {features}\n\n"
            f"📋 What's Included:\n"
            f"• Comprehensive insurance\n"
            f"• 24/7 roadside assistance\n"
            f"• Free delivery within city\n"
            f"• Unlimited mileage\n"
            f"• Full tank of fuel\n\n"
            f"💳 Payment Options:\n"
            f"• M-Pesa (50% deposit)\n"
            f"• Bank transfer\n"
            f"• Cash on delivery\n\n"
            f"{'🎯 Ready to book this car?' if car['available'] else '🔄 Would you like to see similar available cars?'}"
        )

    def generate_booking_form(self, car_id, customer_name):
        car = self.get_car_by_id(car_id)
        if not car:
            return f"Sorry {customer_name}, car not found."

        import math
        deposit_same_day = math.floor(car['price'] * 0.5)
        total_weekend = car['price'] * 2
        deposit_weekend = math.floor(car['price'])
        total_weekly = car['price'] * 6
        deposit_weekly = math.floor(car['price'] * 3)

        return (
            f"📅 Book {car['name']} - {customer_name}\n\n"
            f"🚗 Selected Car: {car['name']}\n"
            f"💰 Daily Rate: TZS {car['price']:,}\n"
            f"📍 Available Locations: {car['location']}\n\n"
            f"⚡ Quick Booking Options:\n\n"
            f"1. Same Day Rental\n"
            f"• Today 2PM - Tomorrow 2PM\n"
            f"• Total: TZS {car['price']:,}\n"
            f"• Deposit: TZS {deposit_same_day:,}\n\n"
            f"2. Weekend Special\n"
            f"• Friday 6PM - Sunday 6PM\n"
            f"• Total: TZS {total_weekend:,}\n"
            f"• Deposit: TZS {deposit_weekend:,}\n\n"
            f"3. Weekly Deal\n"
            f"• 7 days rental\n"
            f"• Total: TZS {total_weekly:,} (1 day FREE!)\n"
            f"• Deposit: TZS {deposit_weekly:,}\n\n"
            f"📝 Or provide custom details:\n"
            f"\"Book from [Date] [Time] to [Date] [Time] at [Location]\"\n\n"
            f"Example: \"Book from Jan 25 9am to Jan 27 6pm at JKIA\"\n\n"
            f"Choose an option below or send custom details!"
        )

    def extract_booking_details(self, message):
        details = {
            'isValid': False,
            'errors': [],
            'pickupDate': None,
            'returnDate': None,
            'pickupLocation': None,
            'customerInfo': {},
            'totalDays': 0,
            'bookingType': 'custom'
        }

        lower_message = message.lower()

        # Handle quick booking options
        if 'same day' in lower_message or 'today' in lower_message:
            details['isValid'] = True
            details['bookingType'] = 'same_day'
            details['pickupDate'] = 'Today 2:00 PM'
            details['returnDate'] = 'Tomorrow 2:00 PM'
            details['pickupLocation'] = 'Main Office'
            details['totalDays'] = 1
            return details

        if 'weekend' in lower_message or 'friday' in lower_message:
            details['isValid'] = True
            details['bookingType'] = 'weekend'
            details['pickupDate'] = 'Friday 6:00 PM'
            details['returnDate'] = 'Sunday 6:00 PM'
            details['pickupLocation'] = 'Main Office'
            details['totalDays'] = 2
            return details

        if 'weekly' in lower_message or 'week' in lower_message:
            details['isValid'] = True
            details['bookingType'] = 'weekly'
            details['pickupDate'] = 'Tomorrow 9:00 AM'
            details['returnDate'] = 'Next Week 9:00 AM'
            details['pickupLocation'] = 'Main Office'
            details['totalDays'] = 7
            return details

        # Handle custom booking details
        if len(message) > 20 and 'book' in lower_message:
            if 'from' in lower_message and 'to' in lower_message:
                details['isValid'] = True
                details['bookingType'] = 'custom'
                details['pickupDate'] = 'As specified'
                details['returnDate'] = 'As specified'
                details['pickupLocation'] = 'As specified'
                details['totalDays'] = 3 # Default
                return details

        details['errors'].append('Please select a quick booking option or provide complete details')
        return details

    def create_booking(self, phone_number, car_id, details, customer_name):
        car = self.get_car_by_id(car_id)
        booking_id = f"BK{int(datetime.datetime.now().timestamp() * 1000)}"
        
        import math
        booking = {
            'id': booking_id,
            'customerId': phone_number,
            'customerName': customer_name,
            'carId': car_id,
            'carName': car['name'],
            'pickupDate': details['pickupDate'],
            'returnDate': details['returnDate'],
            'pickupLocation': details['pickupLocation'],
            'totalDays': details['totalDays'],
            'dailyRate': car['price'],
            'totalAmount': car['price'] * details['totalDays'],
            'deposit': math.floor(car['price'] * details['totalDays'] * 0.5),
            'status': 'confirmed',
            'createdAt': datetime.datetime.now().isoformat(),
            'customerDetails': details['customerInfo']
        }

        self.bookings[booking_id] = booking
        
        # Mark car as temporarily unavailable
        car['available'] = False
        
        return booking

    def generate_booking_confirmation(self, booking, customer_name):
        return (
            f"🎉 Booking Confirmed!\n\n"
            f"Booking ID: {booking['id']}\n"
            f"Customer: {customer_name}\n"
            f"Car: {booking['carName']}\n\n"
            f"📅 Rental Period:\n"
            f"• Pickup: {booking['pickupDate']}\n"
            f"• Return: {booking['returnDate']}\n"
            f"• Duration: {booking['totalDays']} days\n\n"
            f"📍 Pickup Location: {booking['pickupLocation']}\n\n"
            f"💰 Payment Summary:\n"
            f"• Daily Rate: TZS {booking['dailyRate']:,}\n"
            f"• Total Amount: TZS {booking['totalAmount']:,}\n"
            f"• Deposit Due: TZS {booking['deposit']:,}\n\n"
            f"📱 Next Steps:\n"
            f"1. Pay deposit via M-Pesa: 0700123456\n"
            f"2. We'll deliver the car to your location\n"
            f"3. Complete payment on delivery\n\n"
            f"📞 Support: +255683859574\n"
            f"📧 Email: bookings@carrentalpro.com\n\n"
            f"Thank you for choosing CarRental Pro! 🚗✨"
        )

    def generate_category_selection(self, customer_name):
        return (
            f"🚗 Choose Your Car Category, {customer_name}\n\n"
            f"Which type of vehicle are you looking for?\n\n"
            f"💰 Economy Cars - Perfect for city driving\n"
            f"• From TZS 2,500/day\n"
            f"• Fuel efficient and easy to park\n\n"
            f"🚙 SUVs - Great for families and adventures\n"
            f"• From TZS 4,500/day\n"
            f"• Spacious and reliable\n\n"
            f"🏎️ Luxury Cars - Premium experience\n"
            f"• From TZS 8,000/day\n"
            f"• Top-of-the-line features\n\n"
            f"🚐 Vans - Perfect for groups\n"
            f"• From TZS 6,000/day\n"
            f"• Seats up to 14 people\n\n"
            f"Select a category to see available cars!"
        )

    def get_car_category_buttons(self, category):
        cars = self.cars.get(category, [])
        buttons = []
        for index, car in enumerate(cars[:3]):
            buttons.append({
                'id': f"car_{car['id']}",
                'title': f"{index + 1}. {car['name'][:15]}"
            })
        return buttons

    def handle_button_click(self, button_id, session, customer_name, phone_number):
        response = ""
        buttons = None
        message_type = 'interactive_buttons'
        list_items = None
        images = []

        if button_id in ['🚗 Browse Cars', 'browse_cars']:
            response = self.generate_category_selection(customer_name)
            list_items = self.get_category_list_items()
            message_type = 'interactive_list'
            session['state'] = 'selecting_category'

        elif button_id in ['💰 Check Prices', 'check_prices']:
             response = self.generate_pricing_info(customer_name)
             buttons = self.get_category_buttons()
             session['state'] = 'checking_prices'

        elif button_id in ['📋 My Bookings', 'my_bookings']:
            customer_bookings = self.get_customer_bookings(phone_number)
            response = self.generate_booking_status(customer_bookings, customer_name)
            buttons = self.get_booking_management_buttons() if customer_bookings else self.get_main_menu_buttons()
            session['state'] = 'viewing_bookings'

        elif button_id in ['🆘 Get Help', 'get_help']:
            response = self.generate_help_message(customer_name)
            buttons = self.get_help_buttons()
            session['state'] = 'getting_help'

        # Category selections
        elif button_id in ['economy', 'suv', 'luxury', 'van']:
            category = button_id
            response = self.generate_car_catalog(category, customer_name)
            buttons = self.get_car_category_buttons(category)
            
            # Extract images for the cars in this category
            cars = self.cars.get(category, [])[:3] 
            images = [
                {'url': c['image'], 'caption': f"{c['name']} - TZS {c['price']:,}/day"} 
                for c in cars if c.get('image')
            ]
            
            session['state'] = 'browsing_cars'
            session['selectedCategory'] = category

        else:
            if button_id.startswith('car_'):
                car_id = button_id.replace('car_', '')
                car = self.get_car_by_id(car_id)
                if car:
                    response = self.generate_car_details(car, customer_name)
                    buttons = self.get_car_action_buttons(car_id)
                    
                    if car.get('image'):
                        images = [{'url': car['image'], 'caption': car['name']}]
                        
                    session['state'] = 'viewing_car'
                    session['selectedCar'] = car_id
                else:
                    response = self.generate_car_not_found(customer_name)
                    buttons = self.get_main_menu_buttons()

            elif button_id.startswith('book_'):
                car_id = button_id.replace('book_', '')
                response = self.generate_booking_form(car_id, customer_name)
                buttons = self.get_booking_form_buttons()
                session['state'] = 'booking_form'
                session['selectedCar'] = car_id
            
            elif button_id.startswith('pay_'):
                booking_id = button_id.replace('pay_', '')
                booking = self.bookings.get(booking_id)
                if booking:
                    response = self.generate_payment_instructions(booking, customer_name)
                    buttons = self.get_payment_confirmation_buttons(booking_id)
                    session['state'] = 'payment_instructions'

            elif button_id.startswith('confirm_payment_'):
                booking_id = button_id.replace('confirm_payment_', '')
                booking = self.bookings.get(booking_id)
                if booking:
                    response = self.generate_payment_success(booking, customer_name)
                    buttons = self.get_post_payment_buttons()
                    session['state'] = 'booking_complete'
                    booking['status'] = 'paid'
                    booking['paymentDate'] = datetime.datetime.now().isoformat()
            else:
                 response = self.generate_smart_response(button_id, session, customer_name)
                 buttons = self.get_main_menu_buttons()

        self.update_customer_session(phone_number, session)

        return {
            'success': True,
            'response': response,
            'messageType': message_type,
            'buttons': buttons,
            'listItems': list_items,
            'customerName': customer_name,
            'phoneNumber': phone_number,
            'sessionState': session['state'],
            'images': images
        }

    def is_button_click(self, message):
        button_patterns = [
            '🚗 Browse Cars', '💰 Check Prices', '📋 My Bookings', '🆘 Get Help',
            'browse_cars', 'check_prices', 'my_bookings', 'get_help',
            'economy', 'suv', 'luxury', 'van'
        ]
        return (message in button_patterns or 
                message.startswith('car_') or 
                message.startswith('book_') or 
                message.startswith('pay_') or
                message.startswith('confirm_payment_'))

    def is_payment_request(self, message):
        keywords = ['pay', 'payment', 'deposit', 'mpesa', 'bank', 'cash']
        return any(keyword in message.lower() for keyword in keywords)

    def is_payment_confirmation(self, message):
        keywords = ['paid', 'sent', 'transferred', 'completed', 'done', 'confirm']
        return any(keyword in message.lower() for keyword in keywords)

    def generate_payment_instructions(self, booking, customer_name):
        return (
            f"💳 Payment Instructions for {customer_name}\n\n"
            f"Booking ID: {booking['id']}\n"
            f"Car: {booking['carName']}\n"
            f"Total Amount: TZS {booking['totalAmount']:,}\n"
            f"Deposit Required: TZS {booking['deposit']:,}\n\n"
            f"📱 M-Pesa Payment:\n"
            f"• Paybill: 400200\n"
            f"• Account: {booking['id']}\n"
            f"• Amount: TZS {booking['deposit']:,}\n\n"
            f"🏦 Bank Transfer:\n"
            f"• Bank: KCB Bank\n"
            f"• Account: 1234567890\n"
            f"• Name: CarRental Pro Ltd\n"
            f"• Reference: {booking['id']}\n\n"
            f"💵 Cash Payment:\n"
            f"• Visit our office with booking ID\n"
            f"• Pay at pickup location\n\n"
            f"⏰ Payment Deadline: 2 hours from now\n"
            f"📞 Support: +255683859574\n\n"
            f"After payment, click \"Payment Sent\" below."
        )

    ## Helper methods for parsing and state (implementing others briefly)
    
    def get_customer_session(self, phone_number):
        if phone_number not in self.customer_sessions:
            self.customer_sessions[phone_number] = {
                'id': phone_number,
                'state': 'start',
                'messageCount': 0,
                'lastMessage': '',
                'history': [],
                'preferences': {}
            }
        return self.customer_sessions[phone_number]
        
    def update_customer_session(self, phone_number, session):
        self.customer_sessions[phone_number] = session

    def is_greeting(self, message):
        greetings = ['hi', 'hello', 'hey', 'start', 'ambo', 'habari']
        return any(g in message for g in greetings)

    def get_main_menu_buttons(self):
        return [
            {'id': 'browse_cars', 'title': '🚗 Browse Cars'},
            {'id': 'check_prices', 'title': '💰 Check Prices'},
            {'id': 'my_bookings', 'title': '📋 My Bookings'}
        ]

    def is_car_catalog_request(self, message):
         return any(kw in message for kw in ['car', 'browse', 'catalog', 'vehicle'])

    def extract_car_category(self, message):
        for cat in self.cars.keys():
            if cat in message:
                return cat
        return None

    def get_category_list_items(self):
        return [
            {'id': 'economy', 'title': 'Economy', 'description': 'Affordable city cars'},
            {'id': 'suv', 'title': 'SUV', 'description': 'Spacious and rugged'},
            {'id': 'luxury', 'title': 'Luxury', 'description': 'Premium comfort'},
            {'id': 'van', 'title': 'Van', 'description': 'Group travel'}
        ]
        
    def is_car_selection(self, message):
        # Simply checks if message is a digit (1, 2, 3) or starts with car_
        return message.isdigit() or message.strip().startswith('car_')

    def extract_car_id(self, message, category):
        if message.isdigit() and category:
            index = int(message) - 1
            cars = self.cars.get(category, [])
            if 0 <= index < len(cars):
                return cars[index]['id']
        if message.startswith('car_'):
            return message.replace('car_', '')
        return None

    def get_car_by_id(self, car_id):
        for category_cars in self.cars.values():
            for car in category_cars:
                if car['id'] == car_id:
                    return car
        return None

    def get_car_action_buttons(self, car_id):
        return [
            {'id': f'book_{car_id}', 'title': '📅 Book Now'},
            {'id': 'browse_cars', 'title': '🔄 Back to List'}
        ]

    def generate_car_not_found(self, customer_name):
        return f"Sorry {customer_name}, I couldn't find that car. Please try selecting from the list."

    def is_booking_request(self, message):
        return 'book' in message

    def generate_select_car_first(self, customer_name):
        return f"Please select a car first before booking, {customer_name}."

    def get_booking_form_buttons(self):
        return [
            {'id': 'same_day', 'title': 'Same Day'},
            {'id': 'weekend', 'title': 'Weekend Special'},
            {'id': 'custom', 'title': 'Custom Dates'}
        ]

    def is_booking_details(self, message):
        # Simple check if meaningful info provided
        return len(message) > 3

    def generate_booking_form_error(self, errors, customer_name):
        error_msg = "\n".join(errors)
        return f"Oops {customer_name}, something is missing:\n{error_msg}\nPlease try again."

    def get_payment_buttons(self, booking_id):
        return [
            {'id': f'pay_{booking_id}', 'title': '💳 View Payment Info'},
            {'id': 'cancel_booking', 'title': '❌ Cancel'}
        ]

    def get_payment_confirmation_buttons(self, booking_id):
        return [
            {'id': f'confirm_payment_{booking_id}', 'title': '✅ Payment Sent'},
            {'id': 'get_help', 'title': '🆘 Need Help'}
        ]

    def generate_payment_success(self, booking, customer_name):
        return f"Thank you {customer_name}! We have received your payment confirmation for {booking['carName']}. Our team will contact you shortly."

    def get_post_payment_buttons(self):
        return [
            {'id': 'my_bookings', 'title': '📋 View Receipt'},
            {'id': 'main_menu', 'title': '🏠 Main Menu'}
        ]

    def is_price_inquiry(self, message):
        return 'price' in message or 'cost' in message

    def generate_pricing_info(self, customer_name):
        return f"Here are our starting prices:\nEconomy: TZS 2,500\nSUV: TZS 4,500\nLuxury: TZS 8,000"

    def get_category_buttons(self):
        return [
            {'id': 'browse_cars', 'title': 'View Cars'},
            {'id': 'main_menu', 'title': 'Main Menu'}
        ]

    def is_location_inquiry(self, message):
        return 'location' in message or 'where' in message

    def generate_location_info(self, customer_name):
        return f"We are located in Nairobi, Mombasa, and Kisumu. We deliver to airports!"

    def is_help_request(self, message):
        return 'help' in message or 'support' in message

    def generate_help_message(self, customer_name):
        return f"Need help? Call us at +255683859574 or email support@vemacars.com"

    def get_help_buttons(self):
        return [
            {'id': 'main_menu', 'title': 'Back to Menu'}
        ]

    def is_booking_check(self, message):
        return 'booking' in message and ('check' in message or 'my' in message)

    def get_customer_bookings(self, phone_number):
        # Filter bookings for this customer
        return [b for b in self.bookings.values() if b['customerId'] == phone_number]

    def generate_booking_status(self, bookings, customer_name):
        if not bookings:
            return f"You have no active bookings, {customer_name}."
        
        status = f"📋 Booking History for {customer_name}:\n"
        for b in bookings:
            status += f"- {b['carName']} ({b['status']})\n"
        return status

    def get_booking_management_buttons(self):
        return [
            {'id': 'main_menu', 'title': 'Main Menu'}
        ]

    def generate_smart_response(self, message, session, customer_name):
        return f"I didn't quite catch that, {customer_name}. Please use the buttons below."

    def get_contextual_buttons(self, session):
        return self.get_main_menu_buttons()

# Create singleton instance
car_rental_bot_service = CarRentalBotService()
