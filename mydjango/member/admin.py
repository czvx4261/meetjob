from django.contrib import admin

# Register your models here.

from .models import Member # 來自 .models

admin.site.register(Member)