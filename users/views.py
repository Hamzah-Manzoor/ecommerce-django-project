from django.db.models import Count, Sum, Avg
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from const import POST_METHOD
from shops.models import Shop
from orders.models import Order
from .models import User
from django.http import FileResponse, HttpResponseForbidden, Http404
from django.conf import settings
import os


def signup_view(request):
    if request.method == POST_METHOD:
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == POST_METHOD:
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):

    # Query 1: Total orders per customer
    total_orders_per_customer = Order.objects.values('customer__username').annotate(total_orders=Count('id'))
    # SELECT customer.username, COUNT(order.id) AS total_orders
    # FROM order
    # JOIN customer ON order.customer_id = customer.id
    # GROUP BY customer.username;

    # Query 2: Total amount spent per shop, for orders with status 'Delivered'
    total_spent_per_shop = Order.objects.filter(order_status='Delivered').values('shop__name').annotate(total_spent=Sum('total_amount'))
    # SELECT shop.name, SUM(order.total_amount) AS total_spent
    # FROM order
    # JOIN shop ON order.shop_id = shop.id
    # WHERE order.order_status = 'Delivered'
    # GROUP BY shop.name;

    # Query 3: Average order amount for each customer, grouped by shop
    avg_order_amount_per_customer_per_shop = Order.objects.values('customer__username', 'shop__name').annotate(avg_amount=Avg('total_amount'))
    # SELECT customer.username, shop.name, AVG(order.total_amount) AS avg_amount
    # FROM order
    # JOIN customer ON order.customer_id = customer.id
    # JOIN shop ON order.shop_id = shop.id
    # GROUP BY customer.username, shop.name;

    # Query 4: Number of 'Pending' orders per shop
    pending_orders_per_shop = Order.objects.filter(order_status='Pending').values('shop__name').annotate(pending_count=Count('id'))
    # SELECT shop.name, COUNT(order.id) AS pending_count
    # FROM order
    # JOIN shop ON order.shop_id = shop.id
    # WHERE order.order_status = 'Pending'
    # GROUP BY shop.name;

    # Query 5: Orders with total amount greater than the average amount of all orders
    avg_total_amount = Order.objects.aggregate(Avg('total_amount'))['total_amount__avg']
    high_value_orders = Order.objects.filter(total_amount__gt=avg_total_amount)
    # SELECT *
    # FROM order
    # WHERE order.total_amount > (
    #     SELECT AVG(total_amount)
    #     FROM order
    # );

    context = {
        'users': User.objects.filter(role='Customer'),
        'shops': Shop.objects.all(),
        'orders': Order.objects.all(),
        'total_orders_per_customer': total_orders_per_customer,
        'total_spent_per_shop': total_spent_per_shop,
        'avg_order_amount_per_customer_per_shop': avg_order_amount_per_customer_per_shop,
        'pending_orders_per_shop': pending_orders_per_shop,
        'high_value_orders': high_value_orders,
    }
    return render(request, 'users/home.html', context)


@login_required
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get users with the role 'Customer'
        context['users'] = User.objects.filter(role='Customer')
        # Get all shops
        context['shops'] = Shop.objects.all()
        # Get all orders
        context['orders'] = Order.objects.all()
        return context


@login_required
def upload_profile_picture(request):
    if request.method == POST_METHOD and request.FILES['profile_picture']:
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        return redirect('home')  # Replace with your actual home view name

    return render(request, 'users/upload_profile_picture.html')


@login_required
def serve_protected_media(request, path):
    # Get the file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Check if the file belongs to the logged-in user
    user = request.user
    if user.profile_picture and user.profile_picture.name == path:
        return FileResponse(open(file_path, 'rb'))

    return HttpResponseForbidden("You are not allowed to access this file.")

