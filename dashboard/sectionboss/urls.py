from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index_url'),
    path('enter/', views.enter, name='enter_url'),
    path('workers/', views.worker_list, name='workers_list_url'),
    path('enter/exit/', views.enter_exit, name='enter_exit_url'),
    path('workers/<int:id>/', views.worker_detail, name = 'workers_detail_url'),
    path('worker/update/', views.worker_update, name = 'worker_update_url'),
]