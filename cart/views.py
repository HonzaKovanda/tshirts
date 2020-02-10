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
#from products.views import index_view


def anonymous_or_real(request):
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

    messages.info(request, 'Košík byl úspěšně smazán.')
    return redirect("cart:cart_view")




def cart_view(request):

    anonymous_or_real(request)

    user = request.user

    carts = Order.objects.filter(user=user, ordered=False)
    order = [0]
    

    return render(request, "cart/cart_home.html", { 'order':order, 'carts':carts,})

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



def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'password88'
    return HttpResponse("<h1>dataflair<br> the session is set</h1>")
def access_session(request):
    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    if request.session.get('temporary_user_id'):
        response += "Temp user ID : {0} <br>".format(request.session.get('temporary_user_id'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))
        return HttpResponse(response)
    else:
        return redirect('create/')



   


    
