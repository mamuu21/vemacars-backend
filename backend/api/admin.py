from django.contrib import admin
from .models import Car, CarImage, HeroSection, BlogPost, Customer, Invoice, Extra

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 5  # how many empty image slots to show

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    pass

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    pass

from .models import Booking, BookingCustomerInfo

class BookingCustomerInfoInline(admin.StackedInline):
    model = BookingCustomerInfo
    can_delete = False
    verbose_name_plural = 'Customer Info'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'car', 'rental_start', 'rental_end', 'status')
    list_filter = ('status', 'rental_start')
    search_fields = ('reference_code',)
    inlines = [BookingCustomerInfoInline]
