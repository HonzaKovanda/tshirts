from django.test import TestCase

from decouple import config
import requests
from django.urls import reverse

import tempfile

from .apps import get_price_with_tax
from .adler_stock import load_stock, stock_status
from .models import Color, Tshirt, Category, Supplier, ProductsSettings
from .views import create_new_tshirt

from selenium import webdriver


class ProductsTests (TestCase):

    def test_homepage_title(self):
        browser = webdriver.Firefox()
        browser.get('http://localhost:8000')
        assert 'E-shop s tričky' in browser.title

    def test_get_price_with_tax(self):
        DPH = ProductsSettings.objects.create(DPH=21)
        assert get_price_with_tax(100, DPH.DPH) == 100*(DPH.DPH/100 + 1)
    
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



    def create_new_tshirt(self):
        title = 'Basic' 
        slug = 'basic-cerna' 
        price = 200
        category = Category.objects.create()
        supplier = Supplier.objects.create()
        nomen_code="1290116"
        color = Color.objects.create(title='Černá')
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        tshirt = Tshirt.objects.create(title=title, slug=slug, price=price, category=category, supplier=supplier,
        nomen_code=nomen_code, color=color, image=image,)

        assert create_new_tshirt('Basic', 'basic-cerna', 200, '1290116', 'Černá') == tshirt


    def test_products_detail_view(self):
        tshirt = create_new_tshirt('Basic', 'basic-cerna', 200, '1290116', 'Černá')

        response = self.client.get(reverse('products:detail', args=(tshirt.slug,)))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'products/detail.html')


