from django.db import models
from accounts.models import SellerUser

class Category(models.Model):
    name = models.CharField(max_length=32)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE, related_name='products')