from django.urls import path
from .views import *

urlpatterns = [
    path('view/', ProfileViewSet.as_view({'get': 'retrieve'}), name='profile-view'),
    path('update/', ProfileViewSet.as_view({'put': 'update'}), name='profile-update'),
    path('delete/', ProfileViewSet.as_view({'delete': 'destroy'}), name='profile-delete'),
    path('register/', ProfileCreateViewSet.as_view({'post': 'create'}), name='profile-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('shop/', SellerShopView.as_view(), name='seller-shop'),
]