from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Order, Shop
from users.models import User


def order_create_update(request, order_id=None):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        shop_id = request.POST.get('shop')
        total_amount = request.POST.get('total_amount')
        order_status = request.POST.get('order_status')

        customer = get_object_or_404(User, id=customer_id)
        shop = get_object_or_404(Shop, id=shop_id)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order.customer = customer
            order.shop = shop
            order.total_amount = total_amount
            order.order_status = order_status
            messages.success(request, 'Order updated successfully.')
        else:
            order = Order(customer=customer, shop=shop, total_amount=total_amount, order_status=order_status)
            messages.success(request, 'Order created successfully.')

        try:
            order.save()
        except Exception as e:
            messages.error(request, f'Error saving order: {str(e)}')
            return redirect('order_create_update')

        return redirect('order_list')

    users = User.objects.filter(role='Customer')
    shops = Shop.objects.all()
    order = None

    if order_id:
        order = get_object_or_404(Order, id=order_id)

    return render(request, 'users/home.html', {
        'users': users,
        'shops': shops,
        'order': order,
        'orders': Order.objects.all()
    })


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        order.delete()
        messages.success(request, 'Order deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting order: {str(e)}')

    return redirect('order_list')


def order_list(request):
    return order_create_update(request)  # To reuse the order_create_update for listing as well
