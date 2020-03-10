from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'


# Increases price amount by 21% DPH.
def get_price_with_tax(price, dph):
        DPH = 1 + dph/100.0
        price_with_tax = round(float(price) * DPH)
        return price_with_tax
