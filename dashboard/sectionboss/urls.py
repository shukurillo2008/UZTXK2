from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index_url'),
    path('enter/', views.enter, name='enter_url'),
    path('workers/', views.worker_list, name='workers_list_url'),
    path('enter_exit/', views.enter_exit, name='enter_exit_url'),
]