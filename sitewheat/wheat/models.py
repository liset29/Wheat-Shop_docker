from django.db import models


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    unit_price = models.FloatField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    weight = models.FloatField(default=0, blank=False)




class Users(models.Model):
    user = models.ForeignKey('auth.user',models.CASCADE)
    contact_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=11, blank=True)


class Orders(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    order_data = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    weight = models.FloatField(default=0, blank=False)
    city = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=False)
    total_price = models.FloatField(default=0, blank=False)
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        blank=False
    )
    products = models.JSONField()


class Basket(models.Model):
    user = models.ForeignKey('auth.user',models.CASCADE)
    products = models.JSONField()



class Personal(models.Model):
    name = models.CharField(max_length=100, blank=True)


