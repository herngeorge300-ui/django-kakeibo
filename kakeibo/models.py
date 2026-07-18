# kakeiboアプリのデータモデル
# /project2/kakeibo/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    """
        カテゴリークラス
        categorys: カテゴリーの内容
    """
    categorys = models.CharField(max_length=15)
    def __str__(self):
        return self.categorys

class Kakeibo(models.Model):
    """
        家計クラス
        date: 日付
        category: カテゴリー
        money: 金額
        memo: メモ
    """
    # フィールドの定義
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    money = models.IntegerField()
    memo = models.CharField(max_length=30)

    def __str__(self):
        return self.memo
