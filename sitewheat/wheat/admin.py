from django.contrib import admin

from .models import Products,Orders

admin.site.register(Products)
admin.site.register(Orders)