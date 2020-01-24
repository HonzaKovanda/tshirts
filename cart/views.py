#!/usr/bin/python3.8

from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse

from django.contrib import messages

from products.models import Tshirt
from .models import Item, Order

# Adds tshirt to the shopping cart.

def add_to_cart(request, slug):
    item = get_object_or_404(Tshirt, slug=slug)

    this_order = Order.objects.get(user=request.user, ordered=False, active=True)
    item_qs = this_order.orderitems.filter(item=item, user=request.user)

    if item_qs.exists():
        order_item = this_order.orderitems.get(item=item, user=request.user)
    else:
        order_item = Item.objects.create(item=item, user=request.user)

    # Gets existing order or creates new one. 
    # Gets existing tshirt and increases quantity or creates new one.

    order_qs = Order.objects.filter(user=request.user, ordered=False, active=True)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order.
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, 'Počet triček byl navýšen.')
            return redirect("cart:show_active_cart")
        else:
            order.orderitems.add(order_item)
            messages.info(request, 'Tričko bylo úspěšně přidáno do košíku.')
            return redirect("cart:show_active_cart")
    else:
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        order.active = True
        order.save()
        messages.info(request, 'Tričko bylo úspěšně přidáno do košíku.')
        return redirect("cart:show_active_cart")

# Removes tshirt to the shopping cart.

def remove_from_cart(request, slug):
    item = get_object_or_404(Tshirt, slug=slug)
    this_order = Order.objects.get(user=request.user, ordered=False, active=True)
    order_item = this_order.orderitems.get(item=item, user=request.user)

# Gets existed tshirt and decreases quantity or delete it.

    if order_item.quantity > 1:
        order_item.quantity -=1
        order_item.save()
        messages.info(request, 'Tričko bylo odebráno.')
        return redirect("cart:show_active_cart")
    else:
        order_item = Item.objects.get(item=item, user=request.user)
        order_item.delete()
        messages.info(request, 'Tričko bylo odstraněno z košíku.')
        return redirect("cart:show_active_cart")

# Deletes item from shopping cart.

def delete_from_cart(request, slug):
    item = get_object_or_404(Tshirt, slug=slug)
    this_order = Order.objects.get(user=request.user, ordered=False, active=True)
    order_item = this_order.orderitems.get(item=item, user=request.user)
    order_item.delete()
    messages.info(request, 'Tričko bylo odstraněno z košíku.')
    return redirect("cart:show_active_cart")


# Shows items in shopping cart View

def cart_view(request, current_cart):

    user = request.user
    current_cart = int(current_cart)
    current_cart -= 1


    # Deactives all other carts as primary
    orders = Order.objects.filter(user=user, ordered=False)
    for order in orders:
        order.active = False
        order.save()

    # Assigns items to cart
    orders = Order.objects.filter(user=user, ordered=False)
    order = orders[current_cart]
    items = orders[current_cart].orderitems.all()

    # Actives current cart as primary
    order.active = True
    order.save()

    carts = orders

    if items.exists():
        return render(request, 'cart/home.html', {'items': items, 'order': order, 'carts': carts,})
    else:
        messages.warning(request, "Prázdno v košíku jest.")
        return render(request, 'cart/home.html', {'items': items, 'order': order, 'carts': carts,})


def show_active_cart(request):
    user = request.user
    get_carts = Order.objects.filter(user=user, ordered=False,)

    all_carts = []
    for carts in get_carts:
        all_carts.append(carts.id)

    active_cart = Order.objects.get(user=user, ordered=False, active=True)
    active_cart_possition = all_carts.index(active_cart.id)

    return redirect("cart:cart_view", current_cart=int(active_cart_possition+1))


# Creates new cart.

def create_new_cart(request):
    order = Order.objects.create(user=request.user)

    count_all_carts = Order.objects.filter(user=request.user, ordered=False,).count()

    messages.info(request, 'Nový košík vytvořen.')
    return redirect("cart:cart_view", current_cart=count_all_carts)



    
