from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404




class CarList(APIView):
    def get(self, request, format=None):
         # Read mode
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # Validation and creation mode
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class CarDetails(APIView):
    def get_object(self, pk):
        # read mode
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        # retrieve mode
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        # update mode
        car = self.get_object(pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # delete mode
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class BlogList(APIView):
    def get(self, request, format=None):
        #  read mode
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # validation and creation mode
        serializer = BlogPostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class BlogDetails(APIView):
    def get_object(self, pk):
        # read mode
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        # retrieve mode
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        # update mode
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog, data=request.data)
        if seralizer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class HeroSectionView(APIView):
    def get_object(self):
        return get_object_or_404(HeroSection)
    
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
        
    
        
    
class CarImageList(APIView):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        images = car.images.all()
        serializer = CarImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)

        serializer = CarImageSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
        
class CarImageDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(CarImage, pk=pk)

    def get(self, request, pk):
        image = self.get_object(pk)
        serializer = CarImageSerializer(image)
        return Response(serializer.data)

    def patch(self, request, pk):
        image = self.get_object(pk)
        serializer = CarImageSerializer(
            image, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CarImageAllList(APIView):
    def get(self, request):
        images = CarImage.objects.all()
        serializer = CarImageSerializer(images, many=True)
        return Response(serializer.data)



class CustomerList(APIView):
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



class InvoiceList(APIView):
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
