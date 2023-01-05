from django.db import models

# Create your models here.

from django.utils import timezone

# 當 django 要使用圖片上傳功能時
# 要先安裝 pip install pillow 套件

class Photo(models.Model):
    # upload_to= 圖片上船之後，存放的路徑位置
    # blank , null 這兩個表示圖片欄位是否可以為空值，Flase 代表一定要填。
    # 'images/' 是 在 media/images 
    image = models.ImageField(upload_to='images/' , blank = False , null = False)
    
    upload_date = models.DateField(default=timezone.now)