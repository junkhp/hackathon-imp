# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import math


def get_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# def convert_float_to_real_pixels(point_dict, img_width, img_height):
#     return {'x': img_width * point_dict['x'], 'y': img_height * point_dict['y']}


def convert_dict_to_list(mask_points, img_width, img_height):
    out_mask_points = []
    for point in mask_points:
        x = img_width*point['x']
        y = img_height*point['y']
        out_mask_points.append([x, y])
    return out_mask_points


def make_masked_image(img, landmark):
    mask_points = np.array(landmark, dtype=np.int)
    return cv2.fillPoly(img, [mask_points], color=(255, 255, 255))


def generate_masked_image(input_image_path, mask_points):

    # 開発環境用画像パス
    # input_image_path = '/Volumes/disk018/oshiba/hackathon/hackathon-imp/oshiba_test_images/saito.png'
    # input_image_path = '/disk018/share/oshiba/hackathon/hackathon-imp/oshiba_test_images/abe.png'
    # 開発環境用ランドマーク
    # nagahama
    # mask_points = [
    #     {'x': 0.48, 'y': 0.26},
    #     {'x': 0.40, 'y': 0.30},
    #     {'x': 0.41, 'y': 0.35},
    #     {'x': 0.44, 'y': 0.39},
    #     {'x': 0.49, 'y': 0.42},
    #     {'x': 0.55, 'y': 0.40},
    #     {'x': 0.56, 'y': 0.35},
    #     {'x': 0.58, 'y': 0.29},
    # ]

    # # nagahama2
    # mask_points = [
    #     {'x': 0.61, 'y': 0.37},
    #     {'x': 0.49, 'y': 0.40},
    #     {'x': 0.52, 'y': 0.49},
    #     {'x': 0.55, 'y': 0.55},
    #     {'x': 0.61, 'y': 0.59},
    #     {'x': 0.68, 'y': 0.55},
    #     {'x': 0.71, 'y': 0.47},
    #     {'x': 0.73, 'y': 0.39},
    # ]

    # # saito
    # mask_points = [
    #     {'x': 0.48, 'y': 0.36},
    #     {'x': 0.38, 'y': 0.45},
    #     {'x': 0.40, 'y': 0.53},
    #     {'x': 0.46, 'y': 0.58},
    #     {'x': 0.54, 'y': 0.59},
    #     {'x': 0.60, 'y': 0.52},
    #     {'x': 0.61, 'y': 0.42},
    #     {'x': 0.60, 'y': 0.34},
    # ]
    '''
    トレーニングデータから計算
    x座標：127.8867
    y座標：143.3127
    縦長さ(鼻〜あご): 94.48641020153995
    横長さ: 147.61478869547364

    重要点
    鼻：0
    left:1
    rught:7
    ago:4
    '''

    reference_point = [127.8867, 143.3127]
    reference_distance = 147.61478869547364

    # 画像を読み込み
    input_image = cv2.imread(input_image_path)
    # print('入力画像サイズ')
    # print(input_image.shape)

    # 縦の長さと横の長さを取得
    img_height, img_width = input_image.shape[:2]

    # ランドマークを画像上における実際のピクセル値とリストに変換
    mask_points = convert_dict_to_list(mask_points, img_width, img_height)

    # input_image_distance_tate = get_distance()
    input_image_distance_yoko = get_distance(mask_points[1], mask_points[7])

    # リサイズ比を計算
    resize_ratio = reference_distance / input_image_distance_yoko
    # print('リサイズ比')
    # print(resize_ratio)

    # returnするパスを作成
    masked_image_path = input_image_path.replace('.png', '_masked.png')

    # マスクを描画
    filled_image = make_masked_image(input_image, mask_points)

    cv2.imwrite(input_image_path.replace('.png', '_filled.png'), filled_image)

    # リサイズ
    resize_width = int(img_width * resize_ratio)
    resize_height = int(img_height * resize_ratio)
    resized_input_image = cv2.resize(filled_image, (resize_width, resize_height))

    # 200ずつx余白を追加
    black_blank = np.zeros((200, resize_width, 3)).astype(np.uint8)
    # print('black_blankのサイズ')
    # print(black_blank.shape)
    # print('リサイズされた画像のサイズ')
    # print(resized_input_image.shape)
    combined_image = cv2.vconcat([black_blank, resized_input_image, black_blank])

    black_blank = np.zeros((400 + resize_height, 200, 3)).astype(np.uint8)

    combined_image = cv2.hconcat([black_blank, combined_image, black_blank])
    cv2.imwrite(input_image_path.replace('.png', '_combined.png'), combined_image)
    # print('combined_imageのサイズ')
    # print(combined_image.shape)

    # 移動とクロップ
    top_left_x = int(mask_points[0][0]*resize_ratio + 200 - reference_point[0])
    top_left_y = int(mask_points[0][1]*resize_ratio + 200 - reference_point[1])

    top_left = [top_left_x, top_left_y]
    bottom_right = [top_left_x + 256, top_left_y + 256]
    resize_width = img_width * resize_ratio
    resize_height = img_height * resize_ratio
    # print('切り取るときの左上')
    # print(top_left)

    masked_image = combined_image[top_left_y: top_left_y + 256, top_left_x: top_left_x + 256]
    # print('最終的な画像サイズ')
    # print(masked_image.shape)
    # 画像を保存
    cv2.imwrite(masked_image_path, masked_image)

    return masked_image_path, []


if __name__ == "__main__":
    generate_masked_image(0, 0)
