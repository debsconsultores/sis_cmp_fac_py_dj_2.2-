from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic


class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'


class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"