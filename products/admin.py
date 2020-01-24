from django.contrib import admin

from .models import Category, Color, Size, Supplier, Tshirt

# Admin fields formatting.
from django.db import models
from django.forms import TextInput



class TshirtAdmin(admin.ModelAdmin):

    list_display = ['title', 'id', 'nomenklatura', 'category', 'color', 'price', 'supplier', 'created', 'image']

    formfield_overrides = {
    models.IntegerField: {'widget': TextInput(attrs={'size':'40'})},
}


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Supplier)
admin.site.register(Tshirt, TshirtAdmin)