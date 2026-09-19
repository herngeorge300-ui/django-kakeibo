from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, FormView, View
from django.utils import timezone
from .models import Kakeibo,Category
from .forms import PostForm, PostSearchForm, CSVUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
import io

class KakeiboView(ListView):
    model = Kakeibo
    template_name = 'kakeibo/kakeibo.html'
    paginate_by = 5
    def get_queryset(self):
        form = PostSearchForm(self.request.GET or None)
        self.form = form
        queryset = super().get_queryset()
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                for word in key_word.split():
                    queryset = queryset.filter(
                            Q(memo__icontains=word) | Q(category__categorys__icontains=word)
                        )
        return queryset


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

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

class CelDeleteView(LoginRequiredMixin, DeleteView):

    model = Kakeibo
    template_name = "kakeibo/delete.html"

    def get_success_url(self):
        """
        一覧ページにリダイレクト
        """
        return reverse("kakeibo:cel_main")

class KakeiboImport(LoginRequiredMixin, FormView):
    template_name = "kakeibo/import.html"
    success_url = reverse_lazy("kakeibo:cel_main")
    form_class = CSVUpdateForm

    def form_valid(self, form):
        print("Import Succes")
        csvfile = io.TextIOWrapper(form.cleaned_data["file"], encoding="utf-8") #読み込む
        print("Encoding Success")
        df = pd.read_csv(csvfile, encoding="utf-8", usecols=[0,1,2,3], names=["date" ,"category", "money", "memo"],)
        df = df.fillna("")
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        data_np = np.asarray(df)



        for row in data_np:
            defaults = {
                "date" : row[0],
                "category": row[1],
                "money": row[2],
                "memo": row[3]
            }
            data, created = Category.objects.get_or_create(categorys=row[1])
            if not created:
                data.category = row[1]
                data.save()
            Kakeibo.objects.create(date=row[0],category=data,money=row[2],memo=row[3])
        return super().form_valid(form)


class GraphView(View):
    template_name = "kakeibo/script.js"

    def get(self,request, *args):
        category = Category.objects.all()
        kyuuryou = Category.objects.get(categorys='給料')
        kyuuryou2 = Category.objects.get(categorys='臨時収入')
        kakeibo = Kakeibo.objects.filter(~Q(Q(category__exact=kyuuryou.id) | Q(category__exact=kyuuryou2.id)))
        print(kakeibo)
        draft_money = list([data.money for data in kakeibo])
        context = {}
        context["money"] = draft_money
        context["category"] = [data.categorys for data in category if "給料" not in data.categorys if "臨時収入" not in data.categorys]
        return render(request, self.template_name, context, content_type='text/javascript')

class SubGraphView(View):
    template_name = "kakeibo/subscript.js"

    def get(self,request, *args):
        category = Category.objects.all()
        kyuuryou = Category.objects.get(categorys='給料')
        kyuuryou2 = Category.objects.get(categorys='臨時収入')
        kakeibo = Kakeibo.objects.filter(Q(category__exact=kyuuryou.id) | Q(category__exact=kyuuryou2.id))
        draft_money = list([data.money for data in kakeibo])

        context = {}
        context["money2"] = draft_money
        context["category2"] = ["給料","臨時収入"]
        return render(request, self.template_name, context, content_type='text/javascript')
