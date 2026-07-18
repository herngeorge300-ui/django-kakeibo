from django.shortcuts import render, reverse
from django.views.generic import View, CreateView, DetailView, UpdateView
from django.utils import timezone
from .models import Kakeibo
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

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

class CelCreateView(LoginRequiredMixin, CreateView):
    model = Kakeibo
    form_class = PostForm
    template_name = "kakeibo/add.html"

    def form_valif(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return "/"


class CelDetailView(DetailView):
    model = Kakeibo
    template_name = "kakeibo/cel_detail.html"

post_detail = CelDetailView.as_view()

class CelUpdateView(LoginRequiredMixin, UpdateView):
    model = Kakeibo
    form_class = PostForm
    template_name = 'kakeibo/update.html'

    def get_success_url(self):
        return reverse('kakeibo:cel_detail', args=(self.object.id,))
