from django.db import models

# Create your models here.

class Sales(models.Model): # 公司績效
    title = models.CharField(max_length=50)
    info = models.TextField()
    photos = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    create_date = models.DateField(auto_now_add=True) # 只顯示日期
    
    class Meta:
        db_table = 'sales'