from django.urls import path, include

urlpatterns = [
    path('section/', include('dashboard.sectionboss.urls')),
    path('boss/', include('dashboard.boss.urls'))
]