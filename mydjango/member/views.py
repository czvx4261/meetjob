from django.shortcuts import render

import hashlib # 111-11-29 加密用

from .models import Member # 111-11-29

from django.http import HttpResponseRedirect , HttpResponse

# Create your views here.

def login(request):
    msg = ''
    
    if 'email' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        
        # 加密 sha3_256 
        password = hashlib.sha3_256( password.encode('utf-8') ).hexdigest()
        
        obj = Member.objects.filter(email = email , password = password ).count() # 回傳筆數
        
        if obj > 0: # 表示資料表中有這個使用者，且帳密都正確
            # 建立 session 物件
            # 可以將值 暫時儲存在伺服器端，當瀏覽器關閉時，session 內的值，就會不見。
            # 打開瀏覽器時，他會主動跟伺服器端抓取一個 ID ，ID 會不同。
            # 儲存在本地端電腦，稱為 cookies
            
            request.session['myemail'] = email # 儲存 session 資料
            request.session['isAlive'] = True
            
            
            
            # 加上 Cookie 功能，若使用者禁用時，就會失效。
            # 宣告 Cookie 物件
            
            response = HttpResponseRedirect('/')
            # max_age = 秒，在這個範例是 1200秒。
            # 'UMail' 是 自訂變數
            response.set_cookie('UMail' , email , max_age = 1200)
            
            # 111-12-08 設定 Cookie 回傳、跳轉至根目錄
            return response 
        
            # return HttpResponseRedirect('/') # 指向根目錄 (首頁)
        
        else:
            msg = '帳密錯誤！，請重新輸入'
            return render(request , 'login.html' , locals() )
    
    # 如果 myemail 跟 isAlive 的 session 過期了，就回到 login 重新登入
    else:
        if 'myemail' in request.session and 'isAlive' in request.session:
            return HttpResponseRedirect('/member')
        else:
            # 已經登入後，補 Cookie 111-12-08
            myemail = request.COOKIES.get("UMail",'') # 抓取 Cookie 的值，若沒有則空白
            
            return render(request , 'login.html' , locals() )



def logout(request):
    # 刪除 session 內容
    del request.session['isAlive'] 
    del request.session['myemail']
    
    # 第一種
    response = HttpResponseRedirect('/login')
    
    response.delete_cookie('UMail')
    
    return response
    # return HttpResponseRedirect('/login')


    # 第二種寫法，記得上面要 import HttpResponse
    # response = HttpResponse('Delete Cookie')
    # response.delete_cookie('UMail')
    # return HttpResponseRedirect('/login')




def register(request): # 註冊
    msg = ''
    
    if 'userName' in request.POST:
        username = request.POST['userName']
        email = request.POST['email']
        password = request.POST['pwd']
        sex = request.POST['sex']
        birthday = request.POST['birthday']
        address = request.POST['address']
        
        # 使用兩者其中一種，通常都用新的
        
        # 加密 sha256
        # password = hashlib.sha256( password.encode('utf-8') ).hexdigest()
        
        # 加密 sha3_256 
        password = hashlib.sha3_256( password.encode('utf-8') ).hexdigest()
        
        # 此行是要查詢 email ， 是否已存在。
        obj = Member.objects.filter( email = email ).count() # 回傳筆數
        
        if obj == 0: #表示這個 email 沒有註冊過
            # 新增會員資料
            Member.objects.create( name = username , sex = sex , birthday = birthday , email = email , password = password , address = address)
            msg = '已完成註冊！'
        else:
            msg = '此 email 已存在，請換一個 email 註冊'
            
    return render(request , 'register.html' , locals() )


def manage(request):
    
    # 要判斷是否已經登入了，若沒有，就導回去登入
    if 'myemail' in request.session and 'isAlive' in request.session:
        
        msg = ''
        if 'oldpwd' in request.POST:
            oldpwd = request.POST['oldpwd']
            newpwd = request.POST['newpwd']
            
            # 確認使用者輸入的舊密碼是否正確後，將兩個密碼加密
            
            oldpwd = hashlib.sha3_256( oldpwd.encode('utf-8') ).hexdigest()
            newpwd = hashlib.sha3_256( oldpwd.encode('utf-8') ).hexdigest()
            
            # 從 session 抓出來的，因為會員管理你 email 一定有
            email = request.session['myemail']
            
            # 確認使用者輸入的舊密碼是否正確。
            obj = Member.objects.filter( email = email , password = oldpwd).count()
            if obj > 0:
                # 更新密碼
                user = Member.objects.get( email = email)
                user.password = newpwd
                user.save()
                msg = '密碼變更完成'
            else:
                msg = '輸入錯誤，請重新輸入'
    
        return render(request , 'manage.html',locals() )
    
    else:
        return HttpResponseRedirect('/login')










