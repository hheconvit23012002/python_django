from django.db import models

# Create your models here.
class products(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length= 200,unique = True)
    photo = models.ImageField(upload_to='images') 
    desc = models.TextField()
    price = models.FloatField()
    class Meta:
        db_table='products'

class manager(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 100,unique = True)
    password = models.CharField(max_length= 200)
    token = models.CharField(max_length= 200)
    class Meta:
        db_table='manager'
    