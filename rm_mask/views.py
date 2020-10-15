from django.shortcuts import render, redirect
from django.views import generic

from .forms import PhotoForm


def IndexPageView(request):
    template_name = 'rm_mask/index.html'

    if request.method == 'GET':
        request.session.clear()
        params = {
          'form': PhotoForm(),
          'message': '',
        }
        return render(request, template_name, params)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            image_path = form.instance.image.name
            edge_positions = [
              {'x': 0.50, 'y': 0.40},
              {'x': 0.30, 'y': 0.60},
              {'x': 0.30, 'y': 0.75},
              {'x': 0.35, 'y': 0.85},
              {'x': 0.50, 'y': 0.90},
              {'x': 0.65, 'y': 0.85},
              {'x': 0.70, 'y': 0.75},
              {'x': 0.70, 'y': 0.60},
            ]

            request.session['image_path'] = image_path
            request.session['edge_positions'] = edge_positions
            return redirect('mask')
        else:
            params = {
              'form': PhotoForm(),
              'message': 'Error!!',
            }
            return render(request, template_name, params)


def MaskPageView(request):
    template_name = 'rm_mask/mask.html'

    if request.method == 'GET':
        if 'image_path' in request.session and 'edge_positions' in request.session:
            params = {
              'image_path': request.session['image_path'],
              'edge_positions': request.session['edge_positions'],
            }
            return render(request, template_name, params)
        else:
            return redirect('index')

    if request.method == 'POST':
        if 'image_path' in request.session and 'edge_positions' in request.session:
            edge_positions = []
            for i in range(8):
                pos_x = float(request.POST['handle' + str(i) + '_x'])
                pos_y = float(request.POST['handle' + str(i) + '_y'])
                edge_positions.append({'x': pos_x, 'y': pos_y})

            request.session['edge_positions'] = edge_positions
            request.session['output_path'] = request.session['image_path']
            return redirect('result')
        else:
            return redirect('index')


def ResultPageView(request):
    template_name = 'rm_mask/result.html'

    if 'output_path' in request.session:
        params = {
          'output_path': request.session['output_path'],
        }
        return render(request, template_name, params)
    else:
        return redirect('index')