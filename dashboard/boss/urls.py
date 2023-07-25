from django.urls import path
from . import views

urlpatterns = [
    path('index/boss', views.index_boss, name='index_boss_url'),
    path('detail/<int:pk>', views.worker_detail, name='detail_url'),
    path('section/list', views.section_list, name='section_list_url'),
    path('section/create', views.create_section_user, name='section_detail_url'),
    path('section/create', views.create_section_user, name='create_section_url'),
    path('section/update/<int:id>', views.section_update, name='section_update_url'),
    path('section/delate/<int:id>', views.section_delate, name='section_delate_url'),
]
