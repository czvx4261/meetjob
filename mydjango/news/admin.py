from django.contrib import admin

# Register your models here.

from .models import News  # 對應 models

admin.site.register(News)

