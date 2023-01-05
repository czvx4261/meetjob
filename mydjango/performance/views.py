from django.shortcuts import render

# Create your views here.

from .models import Sales

def performance(request):
    data = Sales.objects.all().order_by('-create_date')
    
    return render(request, 'performance.html' , locals())