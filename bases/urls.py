from django.urls import path

from bases.views import Home


urlpatterns = [
    path('',Home.as_view(), name='home'),
]