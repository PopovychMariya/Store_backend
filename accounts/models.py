from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseUser(AbstractUser):
    def is_seller(self):
        return hasattr(self, 'seller_profile')

    def is_customer(self):
        return hasattr(self, 'customer_profile')

class CustomerUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer_profile')

    def __str__(self):
        return self.user.username

class SellerUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(blank=True, null=True, max_length=32)
    store_description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.store_name if self.store_name else self.user.username
