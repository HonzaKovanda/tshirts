from django.db import models

from django.contrib.auth import get_user_model
from products.models import Tshirt, Size, ProductsSettings
from gallery.models import Image

from products.apps import get_price_with_tax




# Get the user model
User = get_user_model()

# Items model
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, default='1')
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tričko {self.item.title}, {self.item.color} - {self.quantity} Ks'

    def get_total(self):
        #return format(self.item.price * self.quantity,",").replace(",", " ")
        return self.item.price * self.quantity

    def get_total_with_tax(self):
        DPH = ProductsSettings.objects.get(pk=1)
        return get_price_with_tax(self.item.price * self.quantity, DPH.DPH)

# Order Model 
class Order(models.Model):
    orderitems = models.ManyToManyField(Item)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Nákupní košík č.: ' + str(self.id) + ' Pacient: ' + self.user.first_name + ' ' + self.user.last_name

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total = total + order_item.get_total()
        
        return total


    def get_totals_with_tax(self):
        total = 0
        DPH = ProductsSettings.objects.get(pk=1)
        for order_item in self.orderitems.all():
            total = total + get_price_with_tax(order_item.get_total(), DPH.DPH)
        
        return total
