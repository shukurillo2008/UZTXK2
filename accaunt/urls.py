from django.urls import path
from . import views

urlpatterns = [
    path('log-in/', views.loginForAdmin, name='login_url'),
    path('log-out/', views.logoutForAdmin, name='logout_url'),
]