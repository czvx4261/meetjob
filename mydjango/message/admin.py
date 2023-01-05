from django.contrib import admin

# Register your models here.

from .models import Message # 對應 models

admin.site.register(Message)