from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminFull, IsStaffOrAdmin, IsAdminOrReadOnly, BookingPermission

# --- CARS ---
# GET -> Public
# POST/PUT/DELETE -> Admin Only

class CarList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CarSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetails(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        car = self.get_object(pk)
        serializer = CarSerializer(car, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(
            car,
            data=request.data,
            context={'request': request},
            partial=True  # 🔥 THIS IS THE KEY
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- BLOGS ---
# GET -> Public
# POST/PUT/DELETE -> Admin Only

class BlogList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, format=None):
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = BlogPostSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetails(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- HERO SECTION ---
# GET -> Public
# PATCH -> Admin Only

class HeroSectionView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        # Ensure at least one object exists
        hero, created = HeroSection.objects.get_or_create(id=1) 
        return hero
    
    def get(self, request, format=None):
        hero = self.get_object()
        serializer = HeroSectionSerializer(hero)
        return Response(serializer.data)
    
    def patch(self, request, format=None):
        hero = self.get_object()
        serializer = HeroSectionSerializer(hero, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- CAR IMAGES ---
# GET -> Public
# POST/PATCH/DELETE -> Admin Only

class CarImageList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        images = car.images.all()
        serializer = CarImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        serializer = CarImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CarImageDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(CarImage, pk=pk)

    def get(self, request, pk):
        image = self.get_object(pk)
        serializer = CarImageSerializer(image)
        return Response(serializer.data)

    def patch(self, request, pk):
        image = self.get_object(pk)
        serializer = CarImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarImageAllList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        images = CarImage.objects.all()
        serializer = CarImageSerializer(images, many=True)
        return Response(serializer.data)


# --- CUSTOMERS ---
# GET/POST/PATCH/DELETE -> Staff or Admin Only

class CustomerList(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get_object(self, pk):
        return get_object_or_404(Customer, pk=pk)

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def patch(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- INVOICES ---
# GET -> Public
# POST/PATCH/DELETE -> Staff or Admin Only

class InvoiceList(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStaffOrAdmin()]

    def get(self, request):
        invoices = Invoice.objects.select_related('customer', 'car')
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStaffOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Invoice, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def patch(self, request, pk):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        invoice = self.get_object(pk)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- BOOKINGS ---
# POST -> Public (create booking)
# GET/PATCH/DELETE -> Staff or Admin Only

class BookingListCreate(APIView):
    def get_permissions(self):
        """
        Custom permissions for Booking List:
        - POST: AllowAny (Anyone can create a booking)
        - GET: IsStaffOrAdmin (Only staff can view all bookings)
        """
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsStaffOrAdmin()]

    def get(self, request):
        bookings = Booking.objects.all().order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates:
        - Booking
        - BookingCustomerInfo
        """
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingDetail(APIView):
    def get_permissions(self):
        """
        - GET: AllowAny (Public can view if they have the ref code)
        - PATCH/DELETE: IsStaffOrAdmin (Only staff can modify)
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStaffOrAdmin()]

    def get_object(self, reference_code):
        return get_object_or_404(Booking, reference_code=reference_code)

    def get(self, request, reference_code):
        booking = self.get_object(reference_code)
        
        # Use Public serializer for anon users, full for staff/admin
        if request.user and (request.user.is_staff or request.user.is_superuser):
            serializer = BookingSerializer(booking)
        else:
            serializer = PublicBookingSerializer(booking)
            
        return Response(serializer.data)

    def patch(self, request, reference_code):
        booking = self.get_object(reference_code)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, reference_code):
        booking = self.get_object(reference_code)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DashboardSummaryView(APIView):
    """
    API View to return counts for Car, Booking, Invoice, and Customer models.
    Only accessible by staff or admins for dashboard card population.
    """
    permission_classes = [IsStaffOrAdmin]

    def get(self, request, *args, **kwargs):
        data = {
            "cars": Car.objects.count(),
            "bookings": Booking.objects.count(),
            "invoices": Invoice.objects.count(),
            "customers": Customer.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)
