from rest_framework import generics, permissions
from .models import Order
from .serializers import *
from accounts.permissions import IsCustomer, IsSeller

class CustomerOrderListView(generics.ListAPIView):
    serializer_class = CustomerOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer_profile)
    
class SellerProductOrderListView(generics.ListAPIView):
    serializer_class = SellerOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Order.objects.filter(product__seller=self.request.user.seller_profile)
    
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CustomerOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)
