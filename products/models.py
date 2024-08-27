from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=32)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    # pictures = models.???())
    # seller = models.???()
    # Are we supposed to use Foreign key here or Many to one relation?
    # I need explanations about the foreign key and how to connect models from different apps.
    # I really want to add many more fields, so I hope the list will get longer in time.
