from django.urls import path

from .views import CategoriaView

urlpatterns = [
    path('categorias/',CategoriaView.as_view(), name='categoria_list'),
]