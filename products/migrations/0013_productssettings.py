# Generated by Django 3.0.2 on 2020-03-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_tshirt_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DPH', models.IntegerField(null=True)),
            ],
        ),
    ]
