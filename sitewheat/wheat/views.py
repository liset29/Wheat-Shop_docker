from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from wheat.forms import OrderForm
from wheat.models import Products, Basket, Users, Orders


class Home(TemplateView):
    template_name = 'wheat/home.html'


class Secret(TemplateView):
    template_name = 'wheat/secret_page.html'

class Founder(TemplateView):
    template_name = 'wheat/founder.html'

class ProductsListView(ListView):
    model = Products
    template_name = 'wheat/products.html'
    context_object_name = 'product_list'


    def get_queryset(self):
        return Products.objects.all()


from django.views.generic import ListView
from wheat.models import Basket, Products


class BasketListView(ListView):
    template_name = 'wheat/basket.html'
    context_object_name = 'basket_products'

    def get_queryset(self):
        user = self.request.user
        basket = Basket.objects.filter(user_id=user.id).first()

        if basket:
            products_in_basket = basket.products or []
            for item in products_in_basket:
                product = Products.objects.get(id=item['product_id'])
                item['product'] = product
            return products_in_basket
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        basket = Basket.objects.filter(user_id=user.id).first()

        if basket:
            total_price = sum(
                item['quantity'] * Products.objects.get(id=item['product_id']).unit_price for item in basket.products)
            total_weight = sum(
                item['quantity'] * Products.objects.get(id=item['product_id']).weight for item in basket.products)
            context['total_price'] = total_price
            context['total_weight'] = total_weight
        else:
            context['total_price'] = 0
            context['total_weight'] = 0

        return context


class OrdersListView(ListView):
    template_name = 'wheat/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user

        # Получаем все заказы пользователя
        orders = Orders.objects.filter(user_id=user.id)

        # Формируем список заказов с продуктами
        products = self.products_in_order(orders)
        print(products)
        return products

    def products_in_order(self, orders):
        products = []

        for order in orders:
            order_data = {
                'id': order.id,
                'status': order.status,
                'created_at': order.order_data,
                'address': order.address,
                'city': order.city,
                'total_price': order.total_price,
                'products': []
            }

            for list_product in order.products:
                product = Products.objects.filter(id=list_product['product_id']).first()
                if product:
                    order_data['products'].append({
                        product.id: {product.product_name: list_product['quantity']}
                    })

            products.append(order_data)

        return products


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from wheat.models import Products, Basket

def add_to_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = request.user

        if user.is_authenticated:
            basket, created = Basket.objects.get_or_create(user=user)
            product = get_object_or_404(Products, id=product_id)
            products_in_basket = basket.products or []

            product_found = False

            for item in products_in_basket:
                if item['product_id'] == product.id:
                    item['quantity'] += 1
                    product_found = True
                    break

            if not product_found:
                products_in_basket.append({'product_id': product.id, 'quantity': 1})

            basket.products = products_in_basket
            basket.save()

            return JsonResponse({'status': 'success', 'message': 'Product added to basket!'})

        else:
            # Если пользователь не авторизован, возвращаем URL для авторизации
            return JsonResponse({
                'status': 'error',
                'message': 'You need to be logged in to add products.',
                'redirect': '/users/login/'  # Замените на ваш URL для страницы авторизации
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def remove_from_basket(request, item_id):
    user = request.user

    if user.is_authenticated:
        basket = Basket.objects.filter(user_id=user.id).first()
        if basket:
            # Удаляем продукт из корзины
            updated_basket = [item for item in basket.products if item['product_id'] != item_id]
            basket.products = updated_basket
            basket.save()
            return JsonResponse({'status': 'success', 'message': 'Product removed from basket!'})
        return JsonResponse({'status': 'error', 'message': 'Basket not found.'})

    return JsonResponse({'status': 'error', 'message': 'You need to be logged in to modify the basket.'})



@method_decorator(login_required, name='dispatch')
class AddPage(CreateView):
    form_class = OrderForm
    template_name = 'wheat/create_order.html'
    title_page = 'Создание заказа'

    def form_valid(self, form):
        order = form.save(commit=False)
        basket = Basket.objects.filter(user_id=self.request.user.id).first()
        self.create_order(order, basket)
        self.add_user_inf(form, order)
        self.decrease_product_quantity(basket)
        basket.products = {}
        basket.save()
        return redirect('home')

    def calculate_total(self, products, field_name):
        total = 0
        for item in products:
            product = Products.objects.filter(id=item['product_id']).first()
            if product:
                total += getattr(product, field_name) * item['quantity']
        return total

    def decrease_product_quantity(self, basket):
        for i in basket.products:
            product = Products.objects.filter(id=i['product_id']).first()
            product.quantity -= i['quantity']
            product.save()

    def create_order(self, order, basket):
        order.user_id = self.request.user.id
        order.total_price = self.calculate_total(basket.products, 'unit_price')
        order.weight = self.calculate_total(basket.products, 'weight')
        order.address = order.address
        order.city = order.city
        order.products = basket.products
        order.save()

    def add_user_inf(self, form, order):
        user = Users.objects.filter(user_id=self.request.user.id).first()
        user.contact_name = form.cleaned_data.get('contact_name', None)
        user.city = order.city
        user.address = order.address
        user.phone = form.cleaned_data.get('phone', None)
        user.save()
