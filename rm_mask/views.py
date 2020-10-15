from django.shortcuts import render, redirect
from django.views import generic

from .forms import PhotoForm


def IndexPageView(request):
    template_name = 'rm_mask/index.html'

    if request.method == 'GET':
        params = {
          'form': PhotoForm(),
          'message': '',
        }
        return render(request, template_name, params)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['image_path'] = form.instance.image.name
            return redirect('index')
        else:
            params = {
              'form': PhotoForm(),
              'message': 'Error!!',
            }
            return render(request, template_name, params)
