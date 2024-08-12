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
    return render(request, 'users/home.html')


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

