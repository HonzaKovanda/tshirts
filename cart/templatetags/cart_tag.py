from django import template
from cart.models import Order

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

        