from django.shortcuts import render , redirect

# Create your views here.

from .forms import UploadModelForm

from .models import Photo



def uploadFile(request):
    photos = Photo.objects.all() # 從資料表抓取目前存放在資料表中的資料
    
    form = UploadModelForm() # 建立上傳圖片物件
    # 可以利用 form
    
    if request.method == 'POST':
        # 這個動作是從網頁中，將檔案準備上傳到伺服器
        form = UploadModelForm(request.POST , request.FILES)
        
        if form.is_valid(): # 是_有效的
            form.save()
            return redirect('/photos')
    
    context = {
        'photos' : photos,
        'form' : form
        }
    return render(request , 'photos.html' , locals() )




    