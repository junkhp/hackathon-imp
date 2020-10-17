import cv2
import sys
sys.path.append("rm_mask/estimate_mask_edge_positions/RetinaFaceAntiCov/")

import numpy as np
import datetime
import os
import glob
from copy import deepcopy
from .RetinaFaceAntiCov.retinaface_cov import RetinaFaceCoV


thresh = 0.8
mask_thresh = 0.2
oscales = [640, 1080]

gpuid = -1 # 負の値にしておくとcpuで動く

#detector = RetinaFaceCoV('./model/mnet_cov1', 0, gpuid, 'net3')
detector = RetinaFaceCoV('rm_mask/estimate_mask_edge_positions/RetinaFaceAntiCov/model/mnet_cov2', 0, gpuid, 'net3l')

flip = False

def face_detecter(img):
    """
    RetinaFaceAntiCovを使って顔のbboxと5点ランドマークを推定する．
    """

    im_shape = img.shape
    target_size = oscales[0]
    max_size = oscales[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    #im_scale = 1.0
    #if im_size_min>target_size or im_size_max>max_size:
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)
    
    scales = [im_scale]
    
    faces, landmark5s = detector.detect(img, thresh, scales=scales, do_flip=flip)

    faces_box = [(left, top, right - left, bottom - top) for left, top, right, bottom, _, _ in faces]

    return faces_box, landmark5s


def katamuki(p, q):
    """
    点p,qを通る直線の傾きを返す 
    """
    dx = p[0]-q[0]
    dy = p[1]-q[1]
    a = dy/dx
    return a

def heikou(z, p):
    """
    傾きのzの直線に平行であり，点pを通る点の直線のパラメータを返す
    """
    x, y = p

    a = z
    b = y - a*x
    return a, b

def chokkou(z, p):
    """
    傾きのzの直線に直交し，点pを通る点の直線のパラメータを返す
    """
    x, y = p

    a = -1/z
    b = y - a*x
    return a, b

def kouten(a1, b1, a2, b2):
    """
    直線の交点を返す．
    """
    x = -(b1-b2)/(a1-a2)
    y = a1 * x + b1
    return x, y

def distance(p, q):
    """
    点pと点qの距離を返す．
    """
    import math
    x1, y1 = p
    x2, y2 = q
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def make_mask_contour(img, face, landmark5):
    """
    5点ランドマークとbboxから8点からなる適当なマスク輪郭を生成する．
    """
    # マスク上部(top), 右端(right), 左端(left),下部右側(bottom_right),下部左側(bottom_left), 下部(bottom)
    # の8点で構成する

    h, w, *_ = img.shape
    f_x, f_y, f_w, f_h = face

    eye_left = landmark5[0]
    eye_right = landmark5[1]
    nose = landmark5[2]
    mouth_left = landmark5[3]
    mouth_right = landmark5[4]

    eye_katamuki = katamuki(eye_left, eye_right)
    nose_line_a, nose_line_b = heikou(eye_katamuki, nose)
    eye_med = (eye_left + eye_right)//2
    eye2nose_distance = distance(eye_med, nose)
    
    eye_nose_r_a, eye_nose_r_b = chokkou(nose_line_a, eye_right)
    h_r_x, h_r_y = kouten(eye_nose_r_a, eye_nose_r_b, nose_line_a, nose_line_b)

    eye_nose_l_a, eye_nose_l_b = chokkou(nose_line_a, eye_left)
    h_l_x, h_l_y = kouten(eye_nose_l_a, eye_nose_l_b, nose_line_a, nose_line_b)
    
    mask_top = (4*eye_left + 4*eye_right + 3*nose) // 11
    # mask_r_x = max(min(2*eye_right[0] - nose[0], w), (f_x+f_w))
    mask_r_x = min(2*h_r_x - nose[0], w)
    mask_r_y = nose_line_a * mask_r_x + nose_line_b - 0.5*eye2nose_distance
    # mask_l_x = min(max(2*eye_left[0]-nose[0], 0), f_x)
    mask_l_x = max(2*h_l_x - nose[0], 0)
    mask_l_y = nose_line_a * mask_l_x + nose_line_b - 0.5*eye2nose_distance
    mask_right = np.array([mask_r_x, mask_r_y])
    mask_left = np.array([mask_l_x, mask_l_y])

    
    eye2jaw_a, eye2_jaw_b = chokkou(eye_katamuki, eye_med)

    mask_b_y = eye_med[1] + 2.5*eye2nose_distance
    mask_b_x = (mask_b_y-eye2_jaw_b)/eye2jaw_a
    
    mask_bottom = np.array([mask_b_x, mask_b_y])

    # 下にはみ出す可能性を考慮
    mask_bottom[1] = max(min(mask_bottom[1], h), f_y + f_h)

    bottom_l_x = (eye_left[0] + 2*mask_left[0])//3
    bottom_l_y = (mask_left[1] + 4*mask_bottom[1])//5
    bottom_r_x = (eye_right[0] + 2*mask_right[0])//3
    bottom_r_y = (mask_right[1] + 4*mask_bottom[1])//5
    mask_bottom_left = np.array([bottom_l_x, bottom_l_y])
    mask_bottom_right = np.array([bottom_r_x, bottom_r_y])

    # 2点補完して6点 -> 8点にするs
    sub_bottom_left = (mask_bottom_left + mask_bottom)/2
    sub_bottom_right = (mask_bottom_right + mask_bottom)/2

    # 時計回りで輪郭作成
    # 6点 ver
    # mask_contour = np.concatenate([mask_top,mask_right, mask_bottom_right, mask_bottom, mask_bottom_left, mask_left])

    mask_contour = np.concatenate([mask_top,mask_right, mask_bottom_right, sub_bottom_right, mask_bottom, sub_bottom_left, mask_bottom_left, mask_left])
    mask_contour = mask_contour.astype(np.int).reshape(-1, 1, 2)

    return mask_contour

def estimate_mask_contour(img):
    """
    本体．画像を入力としてマスクの輪郭を返す．
    """

    # 顔のbboxと5点ランドマークを推定
    faces, landmark5s = face_detecter(img)
    
    if faces:
        face_sizes = [w*h for x, y, w, h in faces]
        face_info = [(face, landmark5, face_size) for face, landmark5, face_size in 
        zip(faces, landmark5s, face_sizes)]
        
        # 一番デカい顔を決める
        face_info.sort(key=lambda x: x[2], reverse=True)
        face, landmark5, _ = face_info[0]

        # 輪郭の推定
        contour = make_mask_contour(img, face, landmark5)
        contour = contour.reshape(-1, 2) # (8, 1, 2) -> (8, 2)
        contour = [(x, y) for x, y in contour]

        return contour

    else:
        # 顔の検出に失敗するとNoneを返す
        return None


def contour_to_edge_positions(contour, img_size):
    """
    輪郭を境界位置に変換
    """
    h, w = img_size
    edge_positions = [{"x":x/w, "y":y/h} for x, y in contour]
    print("detected positions")
    print(edge_positions)
    return edge_positions

def estimate_mask_edge_positions(img_path):
    """
    画像のパスを入力としてマスクの境界位置を返す．
    """

    img = cv2.imread(img_path)
    mask_contour = estimate_mask_contour(img)

    h, w, *_ = img.shape
    mask_edge_positions = contour_to_edge_positions(mask_contour, (h, w))

    return mask_edge_positions


def main():
    print("nanimoshinai")

if __name__ == "__main__":
    main()