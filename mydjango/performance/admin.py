from django.contrib import admin

# Register your models here.

from .models import Sales # 對應 models

admin.site.register(Sales)