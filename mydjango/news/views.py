from django.shortcuts import render

# Create your views here.

from .models import News  # 將 models.py 中的 class 匯入

# 分頁用 函式庫
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def news(request):
    
    #抓資料庫中的所有資料 objects => 資料 , all() => 全部 , order_by 排序 依照欄位名稱 id 來做排序 , - 遞減 若沒有加 (- 號) 時，則為遞增
    #     資料庫.資料.全部().排序("-id")# 遞減排序
    data = News.objects.all().order_by('-id')
    
    
    #分頁
    paginator = Paginator(data , 15) # 25筆為一頁
    page = request.GET.get('page') # 要從網址上的參數抓取資料回來
    try:
        pageData = paginator.page(page) # 抓取目前頁數
    except PageNotAnInteger:
        pageData = paginator.page(1) # 若參數不是整數時，顯示第一頁資料
    except EmptyPage:
        pageData = paginator.page(paginator.num_pages) # num_pages 總頁數(最後一頁) 
    
    
    # 先採用字典方式傳送至網頁
    content = {'newslist':pageData}
    
    # render(request , 網頁名稱 , 參數內容)
    return render(request , 'news.html' , content)


def index(request):
    
    return render(request , 'index.html')










