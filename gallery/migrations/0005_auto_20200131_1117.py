# Generated by Django 3.0.2 on 2020-01-31 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0004_auto_20200131_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='gallery_for_print'),
        ),
        migrations.AlterField(
            model_name='image',
            name='note',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
