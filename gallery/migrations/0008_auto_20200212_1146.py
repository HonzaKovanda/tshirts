# Generated by Django 3.0.2 on 2020-02-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20200207_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='basic_image',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='belongs_to_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]