from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .serializers import *





class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().prefetch_related('images', 'category').order_by('?')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
class ProductNewViewSet(viewsets.ModelViewSet):
    
    queryset = Product.objects.all().order_by('-created_at').prefetch_related('images', 'category')[:10]
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]