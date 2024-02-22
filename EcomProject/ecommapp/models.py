from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    category_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.category_name
    
    
class Products(models.Model):
    product_name=models.CharField(max_length=50)
    price=models.PositiveIntegerField()
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='ecommapp/images')
    description=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField()
    
    def __str__(self):
        return self.product_name
    
    
class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    options=(
        ("in-cart","in-cart"),
        ("order-places","order-places"),
        ("cancelled","cancelled"),
    )
    
    status=models.CharField(max_length=100,choices=options,default="in-cart")
    

class PlaceOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    address=models.CharField(max_length=200)
    order_date=models.DateField(auto_now_add=True)
    options=(
        ("in-cart","in-cart"),
        ("order-places","order-places"),
        ("cancelled","cancelled"),
    )
    
    status=models.CharField(max_length=100,choices=options,default="order-places")
    
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200)