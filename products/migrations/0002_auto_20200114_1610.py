# Generated by Django 3.0 on 2020-01-14 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='tshirt',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Color'),
        ),
    ]
