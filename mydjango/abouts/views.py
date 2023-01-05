from django.shortcuts import render

# Create your views here.
from product.models import Goods
from news.models import News


def aboutme(request):
    
    allnews = News.objects.all().order_by('-id')[:3]
    
    allproduct = Goods.objects.all().order_by('-id')[:3]
    
    return render(request , 'about.html' , locals())