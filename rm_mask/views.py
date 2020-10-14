from django.shortcuts import render
from django.views import generic

class IndexPageView(generic.TemplateView):
    template_name = 'rm_mask/index.html'
