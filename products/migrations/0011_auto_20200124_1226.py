# Generated by Django 3.0.2 on 2020-01-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_color_hexacode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tshirt',
            old_name='nomenklatura',
            new_name='nomen_code',
        ),
        migrations.AddField(
            model_name='color',
            name='nomen_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='size',
            name='nomen_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
