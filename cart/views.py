#!/usr/bin/python3.8

from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic

from django.contrib import messages

from products.models import Tshirt, Size
from .models import Item, Order
from gallery.models import Image

from django.contrib.auth.models import User
from random import randint
from django.contrib.auth import authenticate, login, logout

import typing

def pozdrav(slovo: str) -> str:
    if slovo == 'ahoj':
        vysledek = 'tykani'
    elif slovo == 'dobry den':
        vysledek = 'vykani'
    return vysledek

def check_if_temp_user_exists_and_log_in(request):
    temp_user = request.session.get('temporary_user_id', None)
    if temp_user:
        u = User.objects.get(pk=temp_user)
        return login(request, u)
    else:
        pass

def get_random_number_as_name() -> int:
    return int(randint(1, 100000))

def create_anonymous_user(rand_number: User) -> User:
    u = User(username=rand_number, first_name='User', last_name=rand_number)
    u.set_unusable_password()
    u.save()

    u.username = u.id
    u.save()
    return u

def anonymous_or_real(request):

    check_if_temp_user_exists_and_log_in(request)
    
    user = request.user
    if user.is_authenticated:
        pass
    else:
        rand_number = get_random_number_as_name()
        u = create_anonymous_user(rand_number)

        request.session['temporary_user_id'] = u.id
        return login(request, u)


"""
def anonymous_or_real(request):

    temp_user = request.session.get('temporary_user_id', None)
    if temp_user:
        u = User.objects.get(pk=temp_user)
        login(request, u)


    user = request.user
    if user.is_authenticated:
        return user
    else:
        # if not, create an anonymous user and log them in
        rand_numb = randint(0, 100000)
        username = randint(0, 100000)
        u = User(username=username, first_name='User', last_name=rand_numb)
        u.set_unusable_password()
        u.save()

        u.username = u.id
        u.save()

        request.session['temporary_user_id'] = u.id

        #authenticate(user=u)
        login(request, u)
        return u
"""

def logout_in(request):
    temp_user = request.session.get('temporary_user_id', None)
    logout(request)

    request.session['temporary_user_id'] = temp_user
    return redirect("login")


def migrate_temp_user(request):
    # Check 
    temp_user = request.session.get('temporary_user_id', None)
    if temp_user:
        carts = Order.objects.filter(user=temp_user)
        for cart in carts:
            cart.user = request.user
            cart.save()
            cart_id = cart.id
            active_this_cart(request, cart_id)  

        items = Item.objects.filter(user=temp_user)
        for item in items:
            item.user = request.user
            item.save()

        images = Image.objects.filter(user=temp_user)
        for image in images:
            image.user = request.user
            image.save()

        del request.session['temporary_user_id']
    else: 
        pass
    return redirect("products:home")

def login_by_hash(request, hash):
    u = User.objects.get(password=hash)
    login(request, u)
    return redirect("products:home")


# Sign up
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('cart:logout_in')
    template_name = 'cart/signup.html'


# Adds item from product detail
def add_to_cart_from_detail(request, slug):
    anonymous_or_real(request)
    item_size = Size.objects.get(pk=request.POST['size'])
    return add_to_cart(request, slug, item_size)

# Increases quantity of item in cart
def increase_item(request, slug, item_size, cart_id):
    active_this_cart(request, cart_id)
    return add_to_cart(request, slug, item_size)

# Adds tshirt to the shopping cart.

def add_to_cart(request, slug, item_size):
    item = get_object_or_404(Tshirt, slug=slug) # Gets t-shirt e.g. "classic-bílá"
    item_size = item_size

    this_order, created = Order.objects.get_or_create(user=request.user, ordered=False, active=True)# Gets active cart
    item_qs = this_order.orderitems.filter(item=item, size=item_size, user=request.user)# Gets t-shirt e.g. "classic-bílá" in a active cart

    if item_qs.exists():
        order_item = this_order.orderitems.get(item=item, size=item_size, user=request.user)
    else:
        order_item = Item.objects.create(item=item, size=item_size, user=request.user)
    
    # Gets existing order or creates new one. 
    # Gets existing tshirt and increases quantity or creates new one.

    order_qs = Order.objects.filter(user=request.user, ordered=False, active=True)# Get active cart
    if order_qs.exists(): # If active cart exists
        order = order_qs[0]
        # Check if the order item is in the order.
        if order.orderitems.filter(item__slug=item.slug, size=item_size).exists(): # If in active cart exists t-shirt e.g. "classic-bílá".
            order_item.quantity +=1
            order_item.save()
            messages.info(request, 'Počet triček byl navýšen.')
            return redirect("cart:cart_view")
        else:
            
            # Gets and assigns size of t-shirt from form
            #selected_size = item.size.get(pk=request.POST['size'])
            order_item.size = item_size
            order_item.save()

            # Adds new item 
            order.orderitems.add(order_item)
            messages.info(request, 'Tričko bylo úspěšně přidáno do košíku.')
            return redirect("cart:cart_view")
    else:
        # Gets and assigns size of t-shirt from form
        order_item.size = item_size
        order_item.save()

        # Adds new item 
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        order.active = True
        order.save()
        messages.info(request, 'Tričko bylo úspěšně přidáno do košíku.')
        return redirect("cart:cart_view")

# Removes tshirt to the shopping cart.

def decrease_item(request, slug, item_size, cart_id):
    active_this_cart(request, cart_id)
    item = get_object_or_404(Tshirt, slug=slug)
    item_size = item_size
    this_order = Order.objects.get(user=request.user, ordered=False, active=True)
    order_item = this_order.orderitems.get(item=item, size=item_size, user=request.user)

    # Gets existed tshirt and decreases quantity or delete it.

    if order_item.quantity > 1:
        order_item.quantity -=1
        order_item.save()
        messages.info(request, 'Tričko bylo odebráno.')
        return redirect("cart:cart_view")
    else:
        order_item.delete()
        messages.info(request, 'Tričko bylo odstraněno z košíku.')
        return redirect("cart:cart_view")

# Deletes item from shopping cart.

def delete_item(request, slug, item_size, cart_id):
    active_this_cart(request, cart_id)
    item = get_object_or_404(Tshirt, slug=slug)
    this_order = Order.objects.get(user=request.user, ordered=False, active=True)
    order_item = this_order.orderitems.get(item=item, size=item_size, user=request.user)
    order_item.delete()
    messages.info(request, 'Tričko bylo odstraněno z košíku.')
    return redirect("cart:cart_view")


# Creates new cart.

def create_new_cart(request):
    order = Order.objects.create(user=request.user)

    all_carts = Order.objects.filter(user=request.user, ordered=False,)
    count_all_carts = Order.objects.filter(user=request.user, ordered=False,).count()
    cart_id = all_carts[count_all_carts-1].pk
    
    active_this_cart(request, cart_id)

    messages.info(request, 'Nový košík vytvořen.')
    return redirect("cart:cart_view")


# Deletes particular cart

def delete_cart(request, cart_id):

    cart = Order.objects.get(pk=cart_id)
    items = cart.orderitems.all()
    items.delete()
    cart.delete()

    all_carts = Order.objects.filter(user=request.user, ordered=False,)
    count_all_carts = Order.objects.filter(user=request.user, ordered=False,).count()
    cart_id = all_carts[count_all_carts-1].pk
    
    active_this_cart(request, cart_id)

    messages.info(request, 'Košík byl úspěšně smazán.')
    return redirect("cart:cart_view")




def cart_view(request):

    anonymous_or_real(request)

    user = request.user

    carts = Order.objects.filter(user=user, ordered=False).order_by('created')
    gallery = Image.objects.filter(user=user, basic_image=True).order_by('-created')
    images_in_order = Image.objects.filter(user=user, basic_image=False).order_by('created')

    order = [0]
    anchor = 'active_cart'
    

    return render(request, "cart/cart_home.html", { 'order':order, 'carts':carts, 'gallery':gallery, 'images_in_order':images_in_order, 'anchor':anchor,})

def active_this_cart(request, cart_id):

    user = request.user

    # Deactives all other carts as primary
    orders = Order.objects.filter(user=user, ordered=False)
    for order in orders:
        order.active = False
        order.save()

    # Actives current cart as primary
    order = orders.get(pk=cart_id)
    order.active = True
    order.save()
    return redirect("cart:cart_view")

def active_this_cart_and_home(request, cart_id):
    active_this_cart(request,cart_id)
    return redirect("products:home")


def add_image_to_cart(request, cart_id, image_id):

    user = request.user

    image = Image.objects.get(user=user, pk=image_id)
    image.pk = None
    image.basic_image = False
    image.belongs_to_order = cart_id
    image.save()

    active_this_cart(request, cart_id)
    return redirect("cart:cart_view")

def remove_image_from_cart(request, cart_id, image_id):

    user = request.user

    image = Image.objects.get(user=user, pk=image_id)
    image.delete()

    active_this_cart(request, cart_id)
    return redirect("cart:cart_view")







   


    
