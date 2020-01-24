from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'


# Increases price amount by 21% DPH.
def get_price_with_tax(price):
        DPH = 1.21
        price_with_tax = round(float(price) * DPH)
        return price_with_tax
