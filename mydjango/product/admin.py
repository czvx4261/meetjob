from django.contrib import admin

# Register your models here.

from .models import Goods # .models Goods

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name','price','create_date') # 自訂顯示欄位 , list_display (固定的) 
    # 在 admin 新增資料後，顯示有所不同
    
admin.site.register(Goods,GoodsAdmin)