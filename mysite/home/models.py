
from statistics import mode
from django.db import models
class customers(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 100,unique = True)
    password = models.CharField(max_length= 200)
    token = models.CharField(max_length= 200)
    phone_customer = models.CharField(max_length= 50)
    address_customer = models.CharField(max_length= 100)
    class Meta:
        db_table='customers'
# Create your models here.
class products(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length= 200,unique = True)
    photo = models.ImageField(upload_to='images')  
    desc = models.TextField()
    price = models.FloatField()
    class Meta:
        managed = False
        db_table='products'

class cart(models.Model):
    id_customer = models.ForeignKey(customers, on_delete=models.CASCADE)
    id_product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = ('id_customer', 'id_product')
        db_table='cart'

class order(models.Model):
    id = models.AutoField(primary_key = True)
    id_customer= models.ForeignKey(customers,on_delete=models.CASCADE)
    name_recerver = models.CharField(max_length = 50)
    phone_recerver = models.CharField(max_length = 50)
    address_recerver = models.CharField(max_length = 50)
    status = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add = True)
    sum_price = models.FloatField()
    class Meta:
        db_table ='order'

class order_product(models.Model):
    id_order = models.ForeignKey(order,on_delete=models.CASCADE)
    id_product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = ('id_order', 'id_product')
        db_table = 'order_product'

class rating_product(models.Model):
    id_product = models.ForeignKey(products,on_delete=models.CASCADE)
    id_customer= models.ForeignKey(customers,on_delete=models.CASCADE)
    rating=models.FloatField()
    cmt=models.TextField(default="")
    class Meta:
        unique_together = ('id_product', 'id_customer')
        db_table = 'rating_product'
