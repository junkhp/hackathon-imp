from django.shortcuts import render, redirect
from django.views import generic

from .forms import PhotoForm
from .preprocessing.generate_small_image import generate_small_image
from .generate_masked_image import generate_masked_image
from .generate_masked_image.generate_masked_image import generate_result_image
from .inpainting import Pix2PixModel

import os

from .estimate_mask_edge_positions.estimate_mask_edge_positions import estimate_mask_edge_positions


def IndexPageView(request):
    template_name = 'rm_mask/index.html'

    if request.method == 'GET':
        request.session.flush()
        params = {
            'form': PhotoForm(),
            'message': '',
        }
        return render(request, template_name, params)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            uploaded_image_path = os.path.join('media', form.instance.image.name)
            small_image_path = generate_small_image(uploaded_image_path)

            edge_positions = estimate_mask_edge_positions(small_image_path)

            if edge_positions is None:
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

            request.session['input_image_path'] = small_image_path
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
        if 'input_image_path' in request.session and 'edge_positions' in request.session:
            params = {
                'input_image_path': request.session['input_image_path'],
                'edge_positions': request.session['edge_positions'],
            }
            return render(request, template_name, params)
        else:
            return redirect('index')

    if request.method == 'POST':
        if 'input_image_path' in request.session and 'edge_positions' in request.session:
            edge_positions = []
            for i in range(8):
                pos_x = float(request.POST['handle' + str(i) + '_x'])
                pos_y = float(request.POST['handle' + str(i) + '_y'])
                edge_positions.append({'x': pos_x, 'y': pos_y})

            image_path = request.session['input_image_path']
            masked_image_path, positions = generate_masked_image(image_path, edge_positions)
            p2p = Pix2PixModel(masked_image_path)
            inpainted_image_path = p2p.get_path_to_inpainted_image()

            result_path = generate_result_image(image_path, inpainted_image_path, positions)
            print(result_path)

            request.session['edge_positions'] = edge_positions
            request.session['output_image_path'] = result_path
            return redirect('result')
        else:
            return redirect('index')


def ResultPageView(request):
    template_name = 'rm_mask/result.html'

    if 'output_image_path' in request.session:
        params = {
            'input_image_path': request.session['input_image_path'],
            'output_image_path': request.session['output_image_path'],
        }
        return render(request, template_name, params)
    else:
        return redirect('index')
