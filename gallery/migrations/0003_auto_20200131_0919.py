# Generated by Django 3.0.2 on 2020-01-31 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20200131_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size',
            new_name='title',
        ),
    ]
