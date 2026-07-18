
from django.urls import path
from . import views

app_name = 'kakeibo'
urlpatterns = [
    path('', views.kakeibo, name='cel_main'),
    path('add', views.CelCreateView.as_view(), name='cel_add'),
    path('cel/<int:pk>', views.CelDetailView.as_view(), name="cel_detail"),
    path('cel/<int:pk>/update/', views.CelUpdateView.as_view(), name='cel_update'),
    path('cel/<int:pk>/delete/', views.CelDeleteView.as_view(), name='cel_delete')
]
