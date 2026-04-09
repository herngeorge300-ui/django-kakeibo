
from django.urls import path
from . import views

app_name = 'kakeibo'
urlpatterns = [
    path('', views.kakeibo, name='kakeibo'),
]
