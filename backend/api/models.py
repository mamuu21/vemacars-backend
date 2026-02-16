from django.db import models
import uuid


class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance')
    ]
    FUEL_TYPES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
    ]

    TRANSMISSION_TYPES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    ]
    CAR_TYPES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
    ]

   
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES, default='SUV')
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPES, default='Petrol') 
    seats = models.IntegerField()
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_TYPES, default='Automatic') 
    location = models.CharField(max_length=255)
    
    # Pricing 
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Content for the Details Page
    amenities = models.TextField(help_text="Comma separated list, e.g., A/C, 4WD", null=True, blank=True)
    overview = models.TextField(blank=True, null=True) 
    
    # Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False, help_text="Used for the Car Card display")

    def __str__(self):
        return f"Image for {self.car.name}"
    
  

class HeroSection(models.Model):
    title = models.CharField(max_length=255, default="Finally, Professional Car & Scooter rent possible with Vema Cars")
    ticks = models.TextField(help_text="Enter items separated by a comma (e.g. Simple booking, Quick support)")
    background_image = models.ImageField(upload_to='hero/', null=True, blank=True)
    cta_text = models.CharField(max_length=50, default="Go to Booking")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def save(self, *args, **kwargs):
        if not self.pk and HeroSection.objects.exists():
            raise ValueError("Only one Hero Section is allowed")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Home Page Hero Content"
    
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField() 
   
    is_featured = models.BooleanField(default=False, help_text="Show in the home page swiper")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        
        

    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('dormant', 'Dormant')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    
    ]
    customer = models.ForeignKey(Customer, related_name='invoices', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='invoices', on_delete=models.CASCADE)
    rental_start = models.DateField()
    rental_end = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.name}"
    
    
class Extra(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name



class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    car = models.ForeignKey(Car, related_name='bookings', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extras = models.ManyToManyField(Extra, blank=True)

    rental_start = models.DateField()
    rental_end = models.DateField()

    pickup_location = models.CharField(max_length=255, null=True)
    dropoff_location = models.CharField(max_length=255, null=True)

    # Human-readable reference code (e.g., BOOK-123ABCD)
    reference_code = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rental_days(self):
        """Calculate number of rental days"""
        days = (self.rental_end - self.rental_start).days
        return max(days, 1)

    @property
    def extras_total(self):
        """Calculate total price of selected extras"""
        return sum(self.extras.values_list("price", flat=True))

    @property
    def car_total(self):
        """Calculate total price of car rental"""
        return self.car.price_per_day * self.rental_days

    @property
    def grand_total(self):
        """Calculate grand total (car + extras)"""
        return self.car_total + self.extras_total

    def save(self, *args, **kwargs):
        if not self.reference_code:
            # Generate a unique reference code
            self.reference_code = f"BOOK-{str(uuid.uuid4())[:8].upper()}"
        
        # Initial save to ensure ManyToMany relationships can be handled 
        # (required for first-time save if extras are being set)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Sync total_price from grand_total
        # We do this after super().save() because extras_total needs the ManyToMany relationship
        # which requires a primary key.
        self.total_price = self.grand_total
        
        # Save again to persist the total_price
        # Using update_fields for efficiency if it's not a new record, 
        # but for simplicity and since we might have update logic, we call save() again.
        # super().save(update_fields=['total_price']) is cleaner but grand_total is a property.
        super().save(update_fields=['total_price'])

    def __str__(self):
        return f"Booking {self.reference_code} ({self.status})"


class BookingCustomerInfo(models.Model):
    """
    Stores customer information for a specific booking.
    Decoupled from the main Customer model to allow guest bookings.
    """
    booking = models.OneToOneField(Booking, related_name='customer_info', on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(help_text="Contact email for this booking")
    phone_number = models.CharField(max_length=20)
    
    notes = models.TextField(blank=True, null=True, help_text="Special requests or notes")

    def __str__(self):
        return f"Info for {self.booking.reference_code}"





