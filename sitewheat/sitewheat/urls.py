from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("wheat/", include("wheat.urls")),
    path("admin/", admin.site.urls),
]