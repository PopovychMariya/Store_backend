from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    """
    Custom permission to check if the user is a seller.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seller()

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to check if the user is a customer.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer()

class IsAdminUser(permissions.IsAdminUser):
    """
    Custom permission to check if the user is an admin.
    Inherits from DRF's built-in IsAdminUser.
    """
    pass