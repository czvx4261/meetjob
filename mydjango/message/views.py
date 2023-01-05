from django.shortcuts import render

# Create your views here.

from .models import Message

def contact(request):
    # 如果 'cuName' 存在的話，就把 contact.html 的 name= 帶過去
    if 'cuName' in request.POST:
        cuName = request.POST['cuName']
        email = request.POST['email']
        question = request.POST['question']
        content = request.POST['content']
        
        # 將資料新增至資料表中
        obj = Message.objects.create(name = cuName , 
                                     email = email , 
                                     subject = question , 
                                     content = content)
        obj.save()
    
    return render(request , 'contact.html')