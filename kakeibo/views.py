from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from .models import Kakeibo

class KakeiboView(View):
    def get(self, request, *args, **kwargs):
        """
            Get request用の処理
            家計簿一覧を表示する
        """
        context = {}


        context['kakeibos'] = Kakeibo.objects.all()
        # 記事データを取得
        return render(request, "kakeibo/kakeibo.html", context)

kakeibo = KakeiboView.as_view()
