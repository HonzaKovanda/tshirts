#!/usr/bin/python3.8

from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse

from django.contrib import messages

from products.models import Tshirt, Size
from .models import Item, Order

# Adds item from product detail
def add_to_cart_from_detail(request, slug):
    item_size = Size.objects.get(pk=request.POST['size'])
    return add_to_cart(request, slug, item_size)

# Increases quantity of item in cart
def increase_item(request, slug, item_size, cart_id):
    active_this_cart(request, cart_id)
    return add_to_cart(request, slug, item_size)

# Adds tshirt to the shopping cart.

def add_to_cart(request, slug, item_size):
    item = get_object_or_404(Tshirt, slug=slug) # Vezme tričko, např. classic-bílá
    item_size = item_size

    this_order = Order.objects.get(user=request.user, ordered=False, active=True)# Vezme aktivní košík
    item_qs = this_order.orderitems.filter(item=item, size=item_size, user=request.user)# Vezme např. classic-bílá v aktivním košíku

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


def cart_view(request):
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

    return redirect("products:home")



   


    
