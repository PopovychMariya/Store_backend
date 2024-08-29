from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryListViewSet, basename='category-list')
router.register(r'category', CategoryDetailViewSet, basename='category-detail')


urlpatterns = [
    path('', include(router.urls)),
    path('seller/<int:seller_id>/', SellerProductListView.as_view(), name='seller-product-list'),
    path('my-products/', SellerProductListView.as_view(), name='seller-own-product-list'),
]