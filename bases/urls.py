from django.urls import path
from django.contrib.auth import views as auth_views

from bases.views import Home, HomeSinPrivilegios

from .views import *


urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='bases/login.html'),
        name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='bases/login.html'),
         name='logout'),

    path('sin_privilegios/',
         HomeSinPrivilegios.as_view(),
         name='sin_privilegios'),
    
    path('idiomas/',IdiomaList.as_view(),name="idiomas"),
    path('frases/',FraseList.as_view(),name="frases"),
]