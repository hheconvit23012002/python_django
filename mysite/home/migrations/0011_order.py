# Generated by Django 3.0.8 on 2022-10-20 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20221019_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_recerver', models.CharField(max_length=50)),
                ('phone_recerver', models.CharField(max_length=50)),
                ('address_recerver', models.CharField(max_length=50)),
                ('status', models.IntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('sum_price', models.IntegerField()),
                ('id_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.customers')),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
