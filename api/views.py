from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data
        })
    
    def post(self, request):
        try:
            # Parse JSON data manually từ request body
            if hasattr(request, '_body'):
                raw_data = request._body
            else:
                raw_data = request.body
                
            print("Raw body:", raw_data)
            
            # Parse JSON
            data = json.loads(raw_data)
            print("Parsed data:", data)
            
            serializer = ProductSerializer(data=data)
            
            if serializer.is_valid():
                product = serializer.save()
                return Response({
                    "message": "Product created successfully",
                    "data": ProductSerializer(product).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "Validation error",
                    "errors": serializer.errors,
                    "debug_parsed_data": data
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except json.JSONDecodeError as e:
            return Response({
                "message": "Invalid JSON format",
                "error": str(e),
                "debug_raw_body": str(raw_data)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Server error",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)