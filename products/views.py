from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Product, PricingConfiguration
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@staff_member_required
def pricing_config(request):
    config = PricingConfiguration.get_config()
    return JsonResponse({'mode': config.mode})