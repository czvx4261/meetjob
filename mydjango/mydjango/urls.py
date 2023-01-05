"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# 自行新增 app

from news.views import news , index # 對應 news/
from product.views import shop # 對應 product/

# 111-11-15
from message.views import contact  # message/
from performance.views import performance # performance/
from abouts.views import aboutme 




# 111-11-17 cart , addtocart
# 111-11-22 cartorder , cartok , cartordercheck
# 111-12-01 myorder  我的訂單

# 111-12-01 ECPayCredit 綠界信用卡

from cart.views import cart , addtocart , cartorder , cartok , cartordercheck , myorder , ECPayCredit # ECPayCredit 綠界信用卡




# 111-11-24 login , logout
# 111-11-29 register 註冊
# 111-12-01 manage   # manage 管理 
from member.views import login , logout , register , manage 

# 111-12-06 圖片上傳
from photos.views import uploadFile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('news/' , news),
    path('product/' , shop),
    path('message/' , contact),
    path('performance/' , performance),
    path('about/' , aboutme),
    path('cart/' , cart),

    # 對應 cart.views   , def addtocart
    # 127.0.0.1:8000/addtocart/add/100
    # ctype = add (會新增商品進去) , productid = 10  
    path('addtocart/<str:ctype>/' , addtocart),
    path('addtocart/<str:ctype>/<int:productid>/' , addtocart),
    path('cartorder/' , cartorder),
    path('cartok/' , cartok),
    path('cartordercheck/' , cartordercheck),
    
    # 111-11-24
    path('login/' , login),
    path('logout/' , logout),
    
    # 111-11-29
    path('register/' , register),
    
    # 111-12-01
    path('member/' , manage),
    path('myorder/' , myorder),
    
    # 111-12-01 用於 綠界信用卡付款
    path('creditcard/' , ECPayCredit),
    
    # 111-12-06 圖片上傳
    path('photos/' , uploadFile),
    
    # 111-12-06 首頁，作業自己做
    path('', index ),

]

# 圖片上傳，因為有 DEBUG 會被擋下來，所以要另外設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
















