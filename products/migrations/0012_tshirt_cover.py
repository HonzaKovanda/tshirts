# Generated by Django 3.0.2 on 2020-01-29 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200124_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='tshirt',
            name='cover',
            field=models.BooleanField(default=False),
        ),
    ]
