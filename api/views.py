from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from openai import OpenAI

@api_view(['GET'])
def hello_api(request):
    return Response({
        "message": "Hello World 1 from Django Rest Framework API!",
        "status": "Success",
        "data": {
            "service": "Backend API",
            "version": "1.0"
        }
    })

class ProductListAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data
        })
    elif request.method == 'POST':
        return Response({
            "message": "Product created successfully",
            "data": request.data
        })

@api_view(['GET', 'POST'])
def test_openai(request):
    client = OpenAI(
        base_url="http://192.168.200.135:11434/v1",
        api_key="ollama"
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-oss:20b",
            messages=[
                {"role": "user", "content": "ERPNext dùng cho doanh nghiệp nào?"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        print("✅ Kết nối thành công!")
        print(f"Phản hồi: {resp.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        order = self.get_object()
        order.status = 'completed'
        order.save()
        return Response({'status': 'order completed'})

    @action(detail=False)
    def pending_orders(self, request):
        pending_orders = Order.objects.filter(status='pending')
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)




