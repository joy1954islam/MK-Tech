from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='product/', null=True, blank=True)
    image2 = models.ImageField(upload_to='product/', null=True, blank=True)
    stock = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='pending'
    )
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

    def total_price(self):
        order_id = self.id
        order_price = OrderDetails.objects.filter(order_id=order_id).aggregate(Sum('price'))
        print('price_sum ', order_price)
        return order_price['price__sum']


class OrderDetails(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

