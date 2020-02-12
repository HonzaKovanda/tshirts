from django.urls import path

from . import views

app_name='cart'


urlpatterns = [
    path('registrace/', views.SignUp.as_view(), name='sign_up'),
    path('add_from_detail/<slug>/', views.add_to_cart_from_detail, name='add_item_from_detail'),
    path('create-new-cart/', views.create_new_cart, name='create_new_cart'),
    path('', views.cart_view, name='cart_view'),
    path('active-this-cart/<int:cart_id>/', views.active_this_cart, name='active_this_cart'),
    path('active-this-cart-and-home/<int:cart_id>/', views.active_this_cart_and_home, name='active_this_cart_and_home'),
    path('add/<slug>/<int:item_size>/<int:cart_id>', views.increase_item, name='increase_item'),
    path('add_image_to_cart/<int:cart_id>/<int:image_id>/', views.add_image_to_cart, name='add_image_to_cart'),
    path('remove_image_from_cart/<int:cart_id>/<int:image_id>/', views.remove_image_from_cart, name='remove_image_from_cart'),
    path('remove/<slug>/<int:item_size>/<int:cart_id>', views.decrease_item, name='decrease_item'),
    path('delete/<slug>/<int:item_size>/<int:cart_id>', views.delete_item, name='delete_item'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    path('logout-in/', views.logout_in, name='logout_in'),
    path('migrate_temp_user/', views.migrate_temp_user, name='migrate_temp_user'),
]