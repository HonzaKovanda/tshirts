from django.urls import path

from . import views

app_name='cart'


urlpatterns = [
    path('add_from_detail/<slug>/', views.add_to_cart_from_detail, name='add_item_from_detail'),
    path('create-new-cart/', views.create_new_cart, name='create_new_cart'),
    path('', views.cart_view, name='cart_view'),
    path('active-this-cart/<int:cart_id>/', views.active_this_cart, name='active_this_cart'),
    path('add/<slug>/<int:item_size>/<int:cart_id>', views.increase_item, name='increase_item'),
    path('remove/<slug>/<int:item_size>/<int:cart_id>', views.decrease_item, name='decrease_item'),
    path('delete/<slug>/<int:item_size>/<int:cart_id>', views.delete_item, name='delete_item'),
]