# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:48:00 2022

@author: Administrator
"""

# 
    
from django import forms
from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo 
        fields = ('image',) # 'image' 對應 models
        # 利用這個可以上傳檔案
        widgets = {
            'image':forms.FileInput(attrs={ 'class':'form-control-file'})
            }