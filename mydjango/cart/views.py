from django.shortcuts import render , redirect # redirect 跳轉 

from django.http import HttpResponseRedirect # HttpResponseRedirect 跳轉

from cart import models

from product.models import Goods  # 來自於 根目錄的 product.models 呼叫 Goods   



# 用於 綠界串接，把文字的 html 轉成 網頁的 html
# 111-12-01
from django.utils.html import format_html

# 支付用  111-12-01
# 崁入 ECpay 的 SDK
# 這裡是自己打的，要定位預設目錄
import os
basedir = os.path.dirname(__file__) # 抓取預設目錄位置
file = os.path.join(basedir, 'ecpay_payment_sdk.py')


# 以下是抓 sample_create_order_Credit.py 的內容，有把這個放在 cart 裡面
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    # "/path/to/ecpay_payment_sdk.py"
    file # 上面更改為 file 但是要先打第 16 行
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime






# Create your views here.

cartlist = list() # 購物車內容  空的串列 用於清空及新增

customname = '' # 客戶名稱
customphone = '' # 客戶電話
customaddress = '' # 客戶住址
customemail = '' # 客戶信箱

orderTotal = 0 # 消費金額
goodsTitle = list() # 存入購物車商品名稱

# unit[0]  商品名稱
# unit[1]  價格
# unit[2]  數量
# unit[3]  總價


# 這個是加入至購物車，並未將商品資訊寫入資料庫中
def addtocart( request , ctype = None , productid = None):
    
    global cartlist # global 全域變數
    
    if ctype == 'add': # 將商品加入至購物車中
        product = Goods.objects.get( id = productid ) # 會用get 是因為帶入的產品ID 一定在資料表中
        flag = True # 預設購物車沒有相同的商品，表示購物車內這個商品不存在
        
        
        # 檢查購物車中的商品是否有重複
        
        for unit in cartlist:
            if product.name == unit[0]: # 表示有這個商品
                unit[2] = str( int(unit[2]) + 1 ) # 數量+1
                unit[3] = str( int(unit[3]) + product.price) # 累計金額
                # unit[3] = str( int(unit[2]) * int(unit[1]) ) 這樣也可以

                
                flag = False # 表示商品之前已經加入至購物車中
                break
        
        if flag: # 在購物車中沒有此商品
            templist = list()
            templist.append( product.name )
            templist.append( str(product.price) )
            templist.append( '1' )
            templist.append( str(product.price) )
            cartlist.append(templist)
            
        # unit[0]  商品名稱
        # unit[1]  價格
        # unit[2]  數量
        # unit[3]  總價
        
        
        request.session['cartlist'] = cartlist # 將購物車內容存入到 session 中  ，   session 是可以將資料儲存在伺服器端，當瀏覽器關閉時，資料會被清除
        
        return redirect('/cart/') # 跳轉至此網址
    
    
    
    elif ctype == 'update': # 修改購物車數量
        n = 0
        for unit in cartlist: # 將購物車內容抓出來，並修改數量及總價
            amount = request.POST.get( 'qty' + str(n) , '1') # 抓取 qty0 , qty1 , ... + qty5, 預設數量 1
            if len(amount) == 0:
                amount = '1'
            if int(amount) <= 0:
                amount = '1'
            
            unit[2] = amount
            unit[3] = str( int(unit[1]) * int(unit[2]) ) 
            n += 1
        
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
    elif ctype == 'empty':
        cartlist = list() # 重新指向空的串列
        
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
    elif ctype == 'remove':
        del cartlist[ int(productid) ] # 將加入的商品索引值刪除
        request.session['cartlist'] = cartlist
        return redirect('/cart')
    
    # redirect 直接跳到指定網址去，並沒有帶任何參數過去
    # render 跳到指定網址去，並將要求 (request) 將參數內容傳過去給網頁
    
    
    
    
    
# unit[0]  商品名稱
# unit[1]  價格
# unit[2]  數量
# unit[3]  總價    
    

def cart(request):  # 顯示購物車內容
    global cartlist # 全域變數
    allcart = cartlist
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total + 100 # 預設運費為 100 元
    return render( request , 'cart.html' , locals())


# unit[0]  商品名稱
# unit[1]  價格
# unit[2]  數量
# unit[3]  總價

def cartorder(request): # 結帳
    # 當要結帳時，是要登入後，才可以結帳。 先不做登入
    
    # 111-12-01 補上登入
    if 'myemail' in request.session and 'isAlive' in request.session:
        
        global cartlist , customname , customphone , customaddress , customemail
        
        total = 0
        allcart = cartlist
        for unit in cartlist:
            total += int( unit[3] )
        grandtotal = total + 100 # 加運費
        
        name = customname
        phone = customphone
        address = customaddress
        email = request.session['myemail']
        
        return render(request , 'cartorder.html' , locals() )
    
    else:
        return HttpResponseRedirect('/login')



def cartok(request): # 以確認資料並送出，所以會將訂單寫入到資料庫內
    global cartlist , customname , customphone , customaddress , customemail
    
    global orderTotal , goodsTitle
    
    
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total + 100 # 加運費
    
    orderTotal = grandtotal

    customname = request.POST.get('cuName','')
    customphone = request.POST.get("cuPhone",'')
    customaddress = request.POST.get('cuAddress','')
    customemail = request.POST.get('cuEmail','')
    payType = request.POST.get('payType','')
    
    
    
    #新增資料至訂單資料表中
    unitorder = models.OrdersModel.objects.create(subtotal = total , shipping = 10 , grandtotal = grandtotal , customname = customname , customemail = customemail , customphone = customphone , customaddress = customaddress , paytype = payType)
    
    # 要將各個的商品新增到 明細表中
 
    for unit in cartlist:
        goodsTitle.append(unit[0]) # 將要買的商品名稱新增至 goodTitle 裡面
        total = int( unit[1]) * int( unit[2])


# unit[0]  商品名稱
# unit[1]  價格
# unit[2]  數量

# 要對應 models.DetailModel
# dorder = unitorder 是來自 上面 unitorder
# 用於 連接兩個資料表的方式
        unitdetail = models.DetailModel.objects.create(dorder = unitorder , pname = unit[0] , unitprice = unit[1] , quantity = unit[2] , dtotal = total )

    orderid = unitorder.id # 取得訂單編號
    name = unitorder.customname
    email = unitorder.customemail
    cartlist = list()
    request.session['cartlist'] = cartlist
    
    # 先註解掉， 111-12-01
    # return render(request , 'cartok.html' , locals())
    
    
    if payType == '信用卡':
        return HttpResponseRedirect('/creditcard',locals() ) # 導至信用卡頁
    else:
        return render(request , 'cartok.html' ,locals() )


def cartordercheck(request): # 訂單完成後，可以做訂單查詢
    orderid = request.GET.get('orderid','')
    customemail = request.GET.get('customemail','')
    
    if orderid == '' and customemail == '':
        nosearch = 1 # 沒有抓到
    else:
        order = models.OrdersModel.objects.filter(id = orderid).first() # 抓第一筆資料
        
        if order == None:
            notfound = 1
        else:
            # dorder = 全部帳單明細
            details = models.DetailModel.objects.filter(dorder = order)
    
    return render(request , 'cartordercheck.html' , locals() )
    
    

def myorder(request): # 使用者的訂單
    
    # 判斷 SESSION 是否存在
    # 抓出使用者的購買紀錄
    
    if 'myemail' in request.session and 'isAlive' in request.session:
        email = request.session['myemail']
        
        # get 是資料一定存在才用。 filter 不確定資料是否存在
        order = models.OrdersModel.objects.filter( customemail = email)
        
        return render( request, 'myorder.html' , locals() )
    
    else:
        return HttpResponseRedirect('login.html')
            
        
    


def ECPayCredit(request): # 綠界的信用卡

    global goodsTitle , orderTotal
    title = ''
    for i in goodsTitle:
        title += i + '#'    # 加 # 號，是因為商品若為多個時，要用 # 隔開
    
    # 底下是用複製的 sample_create_order_Credit.py
    # 在 cart 的 資料夾有， C:\meetjob\ECPayAIO_Python-master\sample 裡面也有
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,  # 總額
        'TradeDesc': '訂單測試',
        'ItemName': title,  # 商品名稱
        # 底下改到回聯成官網
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet',
        'ChoosePayment': 'Credit',
        # 底下改到回聯成官網
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        # 底下改到回聯成官網
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }
    
    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html) # 格式化 html ，將文字的 html 轉換為網頁 html
        
        # print(html)  不能用 print
        return render(request , 'paycredit.html' , locals() )
    except Exception as error:
        print('An exception happened: ' + str(error))
    















