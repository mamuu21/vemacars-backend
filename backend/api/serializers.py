from rest_framework import serializers
from .models import *
import json
from django.core.files.base import ContentFile, File



        
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'
        


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'


    def _handle_images(self, instance, request):
        if not request:
            return
            
        # 1. Handle Image Deletions and updates (existing_images)
        existing_images_json = request.data.get('existing_images')
        
        if existing_images_json:
            try:
                existing_images_data = json.loads(existing_images_json)
                if not isinstance(existing_images_data, list):
                    return
                    
                # Find which IDs to keep
                keep_ids = [img.get('id') for img in existing_images_data if img.get('id')]
                # Delete images that are no longer in the list
                instance.images.exclude(id__in=keep_ids).delete()
                
                # Update 'is_primary' status for remaining images
                for img_data in existing_images_data:
                    img_id = img_data.get('id')
                    if img_id:
                        CarImage.objects.filter(id=img_id).update(is_primary=img_data.get('is_primary', False))
            except (json.JSONDecodeError, TypeError):
                pass

        # 2. Handle New Image Uploads
        new_files = request.FILES.getlist('new_images')
        for file in new_files:
            CarImage.objects.create(car=instance, image=file, is_primary=False)

    def create(self, validated_data):
        request = self.context.get('request')
        instance = super().create(validated_data)
        self._handle_images(instance, request)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        instance = super().update(instance, validated_data)
        self._handle_images(instance, request)
        return instance
        
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'
        
        
        
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        # Extract the image from FILES if it exists
        if request and 'image' in request.FILES:
            validated_data['image'] = request.FILES['image']
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        # Check if a new image file was uploaded
        if request and 'image' in request.FILES:
            instance.image = request.FILES['image']
        
        # If the frontend sends 'image' as a string (the existing URL) 
        # and not a file, we should not try to overwrite the existing file.
        # This prevents the "Save error" when you don't change the image.
        if 'image' in validated_data and not isinstance(validated_data['image'], (ContentFile, File)):
            validated_data.pop('image')

        return super().update(instance, validated_data)
        
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
        
        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'


class BookingCustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCustomerInfo
        fields = ['full_name', 'email', 'phone_number', 'notes']



class BookingSerializer(serializers.ModelSerializer):
    customer_info = BookingCustomerInfoSerializer(read_only=True)
    extras = ExtraSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

class PublicBookingSerializer(serializers.ModelSerializer):
    """
    Restricted serializer for public viewing of a booking.
    Hides sensitive customer PII or internal notes if necessary.
    """
    # For now, we show basic info. If you want to hide email/phone, you can use a different CustomerInfo serializer here.
    # But often the user wants to verify their own details. 
    # Let's assume for now we show everything except maybe internal notes if they existed.
    # Actually, let's keep it same as BookingSerializer but we can customize easily later.
    customer_info = BookingCustomerInfoSerializer(read_only=True)
    extras = ExtraSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['reference_code', 'status', 'rental_start', 'rental_end', 'car', 'customer_info', 'created_at']




class BookingCreateSerializer(serializers.ModelSerializer):
    customer_info = BookingCustomerInfoSerializer()
    extras = serializers.PrimaryKeyRelatedField(
        queryset=Extra.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Booking
        fields = [
            "car",
            "rental_start",
            "rental_end",
            "pickup_location",
            "dropoff_location",
            "customer_info",
            "extras"
        ]
        extra_kwargs = {
            'rental_start': {'required': True},
            'rental_end': {'required': True},
        }

    def validate(self, data):
        if data["rental_end"] < data["rental_start"]:
            raise serializers.ValidationError(
                "Rental end date must be after rental start date."
            )
        return data

    def create(self, validated_data):
        extras = validated_data.pop("extras", [])
        customer_data = validated_data.pop("customer_info")

        # Create booking (reference_code + total_price handled in model.save())
        booking = Booking.objects.create(**validated_data)

        # Attach extras
        if extras:
            booking.extras.set(extras)

        # Create nested customer info
        BookingCustomerInfo.objects.create(
            booking=booking,
            **customer_data
        )

        # Trigger recalculation of total_price
        booking.save()

        return booking
