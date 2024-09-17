from django.db import models


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    unit_price = models.FloatField(default=0, blank=False)
    quantity = models.IntegerField(default=0,blank=False)


# class Users(models.Model):
#     contact_name = models.CharField(max_length=100,blank = False)
#     city = models.CharField(max_length=100,blank = False)
#     address = models.CharField(max_length=100,blank = False)
#     phone = models.CharField(max_length=11,blank= False)
#
