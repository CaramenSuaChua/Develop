from django.urls import path
from .views import ProductListAPIView

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.hello_api, name='hello_api'),
    path('products/', views.products, name='products'),
    path('test/', views.test_openai, name='products'),
]
