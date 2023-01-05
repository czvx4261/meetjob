from django.db import models

# Create your models here.

class Goods(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    photo_url = models.CharField(max_length=255)
    good_url = models.CharField(max_length=255)
    discount = models.FloatField() # 折扣
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'goods'
    