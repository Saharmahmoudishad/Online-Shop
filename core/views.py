from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import activate


class IndexView(TemplateView):
    template_name = 'index.html'


class ChangeLangView(View):
    def get(self, request, *args, **kwargs):
        language_code = request.GET.get('lang')
        next_url = request.GET.get('next', '/')

        if language_code:
            activate(language_code)

        return redirect(next_url)
