from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerOrderListView.as_view(), name='customer_orders'),
    path('seller/', SellerProductOrderListView.as_view(), name='seller_orders'),
    path('create/', CreateOrderView.as_view(), name="create_order")
]