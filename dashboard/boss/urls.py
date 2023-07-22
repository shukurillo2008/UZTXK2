from django.urls import path
from . import views

urlpatterns = [
    path('index/boss', views.index_boss, name='index_boss_url'),
    path('detail/<int:pk>', views.worker_detail, name='detail_url'),
]
