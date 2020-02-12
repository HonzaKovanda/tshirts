from django import template
from cart.models import Order
from gallery.models import Image

register = template.Library()

@register.filter
def cart_total(user):
    orders = Order.objects.filter(user=user, ordered=False)
    total = 0

    if orders.exists():
        for order in orders:
            for item in order.orderitems.all():
                total += item.quantity
        return total
    else:
    	return 0

@register.filter
def number_of_images_in_cart(cart_id):

    number_of_images_in_cart = Image.objects.filter(belongs_to_order=cart_id).count()
    return number_of_images_in_cart
