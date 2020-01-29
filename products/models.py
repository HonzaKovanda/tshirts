from django.db import models

from products.apps import get_price_with_tax


class Category(models.Model):
    sex = models.CharField(max_length=50)

    def __str__(self):
        return self.sex

class Color(models.Model):
    title = models.CharField(max_length=50)
    hexacode = models.CharField(max_length=50, null=True)
    nomen_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

class Size(models.Model):
    title = models.CharField(max_length=10)
    nomen_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

class Supplier(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Tshirt(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    slug = models.SlugField()
    cover = models.BooleanField(default=False)
    nomen_code = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    size = models.ManyToManyField(Size)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default='1')
    image = models.ImageField(upload_to='gallery')  
    price = models.DecimalField(max_digits=25, decimal_places=0)
    created = models.DateTimeField('Created', auto_now_add=True)

    def __str__(self):
        return self.title

    def price_with_tax(self):
        return get_price_with_tax(self.price)






