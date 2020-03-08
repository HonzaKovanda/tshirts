from django.test import TestCase


from decouple import config
import requests
from django.urls import reverse

import tempfile

from .apps import get_price_with_tax
from .adler_stock import load_stock, stock_status
from .models import Color, Tshirt, Category, Supplier


class ProductsTests (TestCase):

    def test_get_price_with_tax(self):
        DPH = 1.21
        assert get_price_with_tax(100) == (100*DPH)
    
    def test_load_stock(self):
        r = requests.get(config('ADLER_JSON'))
        data = r.json()
        assert load_stock() == data

    def setUp(self):
        Color.objects.create(title='Černá')

    def test_color_title(self):
        color = Color.objects.get(id=1)
        expected_object_name = f'{color.title}'
        self.assertEquals(expected_object_name, 'Černá')

    def test_products_home_view(self):
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')

    def test_products_detail_view(self):
        category = Category.objects.create()
        Supplier.objects.create()
        color = Color.objects.get(id=1)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        tshirt = Tshirt.objects.create(title='Pure', slug='pure-cerna', price=200, category=category, 
        nomen_code="1220115", color=color, image=image,)

        response = self.client.get(reverse('products:detail', args=(tshirt.slug,)))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'products/detail.html')


