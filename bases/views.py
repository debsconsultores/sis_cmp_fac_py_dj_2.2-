from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic


class SinPrivilegios(PermissionRequiredMixin):
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'


class HomeSinPrivilegios(generic.TemplateView):
    template_name="bases/sin_privilegios.html"