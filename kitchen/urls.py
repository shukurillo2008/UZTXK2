from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='kitchen_index_url'),    
]