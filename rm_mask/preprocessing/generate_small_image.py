# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import math

def get_add_path(original_path, add_word):
    '''
    パスの画像名を変更
    例
    get_add_path('images/test.png', 'masked')
    なら
    'images/test_masked.png'
    が出力される
    '''
    file_name, ext = os.path.splitext(original_path)
    out_path = file_name + '_' + add_word + ext
    return out_path


def generate_small_image(uploaded_image_path):
    small_image_path = get_add_path(uploaded_image_path, 'small')
    print(small_image_path)
    uploaded_image = cv2.imread(uploaded_image_path)
    height, width = uploaded_image.shape[:2]

    if height > width:
        scaledWidth = int(width * 650 / height)
        small_image = cv2.resize(uploaded_image, (scaledWidth, 650))
    else:
        scaledHeight = int(height * 650 / width)
        small_image = cv2.resize(uploaded_image, (650, scaledHeight))

    cv2.imwrite(small_image_path, small_image)

    return small_image_path
