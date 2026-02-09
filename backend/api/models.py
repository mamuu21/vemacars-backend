from django.db import models


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