from django.urls import path

from . import views

app_name='cart'


urlpatterns = [
    path('add/<slug>/', views.add_to_cart, name='add_item'),
    path('<int:current_cart>/', views.cart_view, name='cart_view'),
    path('active_cart/', views.show_active_cart, name='show_active_cart'),
    path('create_new_cart/', views.create_new_cart, name='create_new_cart'),
    path('remove/<slug>/', views.remove_from_cart, name='remove'),
    path('delete/<slug>/', views.delete_from_cart, name='delete'),
]