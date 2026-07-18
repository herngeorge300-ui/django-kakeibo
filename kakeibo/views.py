from django.shortcuts import render, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.utils import timezone
from .models import Kakeibo
from .forms import PostForm, PostSearchForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class KakeiboView(ListView):
    model = Kakeibo
    template_name = 'kakeibo/kakeibo.html'
    paginate_by = 3
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
