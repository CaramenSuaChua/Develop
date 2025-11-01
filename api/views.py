from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from urllib.parse import unquote
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
            print("Request content type:", request.content_type)
            print("Request POST data:", request.POST)
            print("Request data:", request.data)
            
            # Xử lý cả form data và JSON
            if request.content_type == 'application/x-www-form-urlencoded':
                # Extract từ form data
                content_type = request.POST.get('_content_type', '')
                json_content = request.POST.get('_content', '')
                
                if json_content:
                    # URL decode và parse JSON
                    decoded_content = unquote(json_content)
                    print("Decoded content:", decoded_content)
                    data = json.loads(decoded_content)
                else:
                    # Nếu là form data thông thường
                    data = {
                        'name': request.POST.get('name'),
                        'price': request.POST.get('price')
                    }
            else:
                # Nếu là JSON raw
                data = request.data
            
            print("Final data for serializer:", data)
            
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
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except json.JSONDecodeError as e:
            return Response({
                "message": "Invalid JSON format in _content",
                "error": str(e),
                "debug_raw_post": dict(request.POST)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Server error",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)