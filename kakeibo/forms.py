from django.forms import ModelForm
from .models import Kakeibo

class PostForm(ModelForm):
    class Meta:
        model = Kakeibo

        fields = ("date", "category", 'money', 'memo')
        labels = {
            'date': '日付',
            'category': 'カテゴリー',
            'money': '金額',
            'memo': 'メモ',
        }
