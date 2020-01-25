from django.urls import path

from . import views

app_name='cart'


urlpatterns = [
    path('add_from_detail/<slug>/', views.add_to_cart_from_detail, name='add_item_from_detail'),
    path('add/<slug>/<int:item_size>/', views.add_to_cart, name='add_item'),
    path('<int:current_cart>/', views.cart_view, name='cart_view'),
    path('active_cart/', views.show_active_cart, name='show_active_cart'),
    path('create_new_cart/', views.create_new_cart, name='create_new_cart'),
    path('remove/<slug>/<int:size>/', views.remove_from_cart, name='remove'),
    path('delete/<slug>/<int:size>/', views.delete_from_cart, name='delete'),
]