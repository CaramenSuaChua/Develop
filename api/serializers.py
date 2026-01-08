# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        print("Raw data received:", data)  # Debug: xem dữ liệu nhận được
        return super().to_internal_value(data)