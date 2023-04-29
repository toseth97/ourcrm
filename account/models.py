from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    profile_pix = models.ImageField(
        default="default_user.png", null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('indoor', 'indoor'),
        ('outdoor', 'outdoor')
    )
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.TextField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=200, null=True, choices=STATUS, default=STATUS[0][0])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
