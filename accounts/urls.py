from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/metadata/<str:user_type>/', RegistrationMetadataView.as_view(), name='registration-metadata'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]