from django.contrib import admin
from .models import BaseUser, CustomerUser, SellerUser

'''class CustomerUserInline(admin.StackedInline):
    model = CustomerUser
    can_delete = False

class SellerUserInline(admin.StackedInline):
    model = SellerUser
    can_delete = False'''

@admin.register(BaseUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    pass

@admin.register(SellerUser)
class SellerUserAdmin(admin.ModelAdmin):
    pass