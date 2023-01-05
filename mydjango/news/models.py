from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=254)
    photo = models.CharField(max_length=254)
    create_date = models.DateField(auto_now_add=True) # 自動放入當下日期
    
    class Meta:
        db_table = 'news'