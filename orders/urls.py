from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.order_create_update, name='order_create_update'),
    path('order/<int:order_id>/', views.order_create_update, name='order_edit'),
    path('order/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('orders/', views.order_list, name='order_list'),
]
