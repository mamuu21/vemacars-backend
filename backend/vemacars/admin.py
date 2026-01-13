from django.contrib import admin
from .models import Car, CarImage, HeroSection, BlogPost

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