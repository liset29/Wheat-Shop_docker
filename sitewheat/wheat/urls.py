from django.urls import path

from . import views
from .views import add_to_basket, remove_from_basket

urlpatterns = [
    # path('products/', views.ProductsListView.as_view(), name='products_list'),
    path('add_to_basket/', add_to_basket, name='add_to_basket'),
    path('basket/', views.BasketListView.as_view()),
    path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('checkout/', views.remove_from_basket),
    path('create_order/', views.AddPage.as_view(), name='create_order'),


    path('home/', views.Home.as_view(), name='home'),
    path('products/', views.ProductsListView.as_view(), name='products'),
    path('basket/',views.BasketListView.as_view(),name = 'basket'),
    path('orders/',views.OrdersListView.as_view(), name = 'orders'),
    path('remove_from_basket/<int:item_id>/', remove_from_basket, name='remove_from_basket'),
    path('create_order/', views.AddPage.as_view(), name='create_order'),
    path('founder/',views.Founder.as_view(),name = 'founder'),
    path('secret_page/',views.Secret.as_view(),name = 'secret_page')


]
