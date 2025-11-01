from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(APIView):
    authentication_classes = []  # Tắt authentication tạm thời
    permission_classes = [AllowAny]  # Cho phép mọi request
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data
        })
    
    def post(self, request):
        print("=== DEBUG INFO ===")
        print("Request data:", request.data)
        print("Request headers:", dict(request.headers))
        
        serializer = ProductSerializer(data=request.data)
        print("Serializer initial data:", serializer.initial_data)
        
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "message": "Product created successfully",
                "data": ProductSerializer(product).data
            }, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response({
                "message": "Validation error", 
                "errors": serializer.errors,
                "debug_received_data": str(request.data)  # Thêm debug info
            }, status=status.HTTP_400_BAD_REQUEST)