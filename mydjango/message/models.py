from django.db import models

# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50) # 主旨
    content = models.TextField() # 內容
    create_date = models.DateTimeField(auto_now_add=True) #顯示日期、時間 ， 自行新增
    
    class Meta:
        db_table = 'contact'