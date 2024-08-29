from django.contrib import admin
from .models import BaseUser, CustomerUser, SellerUser


@admin.register(BaseUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    pass

@admin.register(SellerUser)
class SellerUserAdmin(admin.ModelAdmin):
    pass