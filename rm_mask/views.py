from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .forms import PhotoForm

class IndexPageView(generic.CreateView):
    template_name = 'rm_mask/index.html'
    form_class = PhotoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        print('image path: ' + form.instance.image.name)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
