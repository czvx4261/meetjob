from django.db import models

# Create your models here.

# default => 默認

class OrdersModel(models.Model):
    subtotal = models.IntegerField(default = 0) #小計
    shipping = models.IntegerField(default = 0) #運費
    grandtotal = models.IntegerField(default = 0) #累計
    customname = models.CharField(max_length = 100) #顧客名稱
    customemail = models.CharField(max_length = 100) # 顧客信箱
    customphone = models.CharField(max_length = 50) #顧客電話
    paytype = models.CharField(max_length = 20) #支付方式
    create_date = models.DateTimeField(auto_now_add = True) #建立時間
    customaddress = models.CharField(max_length=200)
    
    def __str__(self):
        return self.customname
    
class DetailModel(models.Model):
    # ForeignKey => 讓他們兩個資料表有關聯  ；  當 前者資料被刪除，後者也會
    dorder = models.ForeignKey('OrdersModel' , on_delete = models.CASCADE) # 訂單
    pname = models.CharField(max_length = 100) #單一商品名稱
    unitprice = models.IntegerField(default = 0) #單一商品價格
    quantity = models.IntegerField(default = 0) #數量
    dtotal = models.IntegerField(default = 0) #商品全部金額
    
    def __str__(self):
        return self.pname
    
    
    
    
    
    
    