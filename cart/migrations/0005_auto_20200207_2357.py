# Generated by Django 3.0.2 on 2020-02-07 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_tshirt_cover'),
        ('cart', '0004_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Size'),
        ),
    ]
