#kakeiboアプリのAdmin設定
#/project2/kakeibo/admin.py

from django.contrib import admin
from .models import Kakeibo, Category

admin.site.register(Kakeibo)
admin.site.register(Category)
