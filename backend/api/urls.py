from django.urls import path
from .views import *

urlpatterns = [
    # Cars
    path('cars/', CarList.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarDetails.as_view(), name='car-detail'),

    # Car Images
    path('car/<int:car_id>/images/', CarImageList.as_view(), name='car-image-list'),
    path('car-images/', CarImageAllList.as_view(), name='car-image-all'),
    path('car-images/<int:pk>/', CarImageDetail.as_view(), name='car-image-detail'),

    # Blogs
    path('blogs/', BlogList.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetails.as_view(), name='blog-detail'),

    # Hero Section (singleton)
    path('hero/', HeroSectionView.as_view(), name='hero-section'),

    # Customers
    path('customers/', CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),

    # Invoices
    path('invoices/', InvoiceList.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', InvoiceDetail.as_view(), name='invoice-detail'),
]
