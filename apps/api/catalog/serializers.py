from rest_framework import serializers

from apps.catalog.models import Category, Product, Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
