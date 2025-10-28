

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['GET'])
def hello_api(request):
    return Response({
        "message": "Hello World test121211 from Django Rest Framework API!",
        "status": "Success",
        "data": {
            "service": "Backend API",
            "version": "1.0"
        }
    })

@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        return Response({
            "products": [
                {"id": 1, "name": "Product A", "price": 29.99},
                {"id": 2, "name": "Product B", "price": 39.99},
                {"id": 3, "name": "Product C", "price": 49.99}
            ]
        })
    elif request.method == 'POST':
        return Response({
            "message": "Product created successfully",
            "data": request.data
        })




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
