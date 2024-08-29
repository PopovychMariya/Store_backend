from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import CustomerUser

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='orders')
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.customer.user.username} (x{self.quantity})"