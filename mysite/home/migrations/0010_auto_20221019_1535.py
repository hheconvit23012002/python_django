# Generated by Django 3.0.8 on 2022-10-19 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20221019_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.customers'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.products'),
        ),
    ]
