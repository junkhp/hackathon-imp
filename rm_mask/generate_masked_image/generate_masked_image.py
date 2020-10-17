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


def generate_masked_image(input_image_path, mask_points):
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
    masked_image_path = get_add_path(input_image_path, 'masked')

    # マスクを描画
    filled_image = make_masked_image(input_image, mask_points)

    cv2.imwrite(get_add_path(input_image_path, 'filled'), filled_image)

    # リサイズ
    resize_width = int(img_width * resize_ratio)
    resize_height = int(img_height * resize_ratio)
    resized_input_image = cv2.resize(filled_image, (resize_width, resize_height))
    resized_input_image_path = get_add_path(input_image_path, 'resized')
    cv2.imwrite(resized_input_image_path, resized_input_image)

    # 200ずつx余白を追加
    black_blank = np.zeros((200, resize_width, 3)).astype(np.uint8)
    # print('black_blankのサイズ')
    # print(black_blank.shape)
    # print('リサイズされた画像のサイズ')
    # print(resized_input_image.shape)
    combined_image = cv2.vconcat([black_blank, resized_input_image, black_blank])

    black_blank = np.zeros((400 + resize_height, 200, 3)).astype(np.uint8)

    combined_image = cv2.hconcat([black_blank, combined_image, black_blank])
    cv2.imwrite(get_add_path(input_image_path, 'combined'), combined_image)
    # print('combined_imageのサイズ')
    # print(combined_image.shape)

    # 移動とクロップ
    top_left_x = int(mask_points[0][0]*resize_ratio + 200 - reference_point[0])
    top_left_y = int(mask_points[0][1]*resize_ratio + 200 - reference_point[1])

    top_left_combined = [top_left_x-200, top_left_y-200]
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
    crop_params_dict = {
        'input_image_path': input_image_path,
        'resize_ratio': resize_ratio,
        'top_left': top_left_combined,
        'resized_input_image_path': resized_input_image_path,
    }
    print(crop_params_dict)

    return masked_image_path, crop_params_dict


def generate_result_image(image_path, inpainted_image_path, crop_params_dict):
    final_result_path = get_add_path(image_path, 'final_result')
    back_image = cv2.imread(image_path)
    resized_back_image = cv2.imread(crop_params_dict['resized_input_image_path'])
    print('背景画像のサイズ')
    print(back_image.shape)
    inpainted_image = cv2.imread(inpainted_image_path)

    resize_ratio = crop_params_dict['resize_ratio']
    top_left = crop_params_dict['top_left']
    top_left_relocate = [top_left[0] / resize_ratio, top_left[1] / resize_ratio]
    img_size = 256 / resize_ratio

    '''背景画像をリサイズしないやり方'''
    # ToDo:リサイズのアルゴリズムの検討
    # inpainted_image_resized = cv2.resize(inpainted_image, (int(img_size), int(img_size)))

    # print('リサイズ後のインペイント画像のサイズ')
    # print(inpainted_image_resized.shape)

    # back_image[int(top_left_relocate[1]): int(top_left_relocate[1]) + int(img_size),
    #            int(top_left_relocate[0]): int(top_left_relocate[0]) + int(img_size)] = inpainted_image_resized
    # cv2.imwrite(final_result_path, back_image)

    '''背景画像をリサイズするやり方'''

    resized_back_image[int(top_left[1]): int(top_left[1]) + 256,
                       int(top_left[0]): int(top_left[0]) + 256] = inpainted_image

    print('インペイント画像のサイズ')
    print(inpainted_image.shape)
    print('小さい背景画像サイズ')
    print(resized_back_image.shape)

    cv2.imwrite(final_result_path, resized_back_image)

    # return final_result_path
    return inpainted_image_path

# if __name__ == "__main__":
#     # generate_masked_image(0, 0)
#     print(get_add_path('/kjfd/oshoi/fhido/junki.jpeg', 'mask'))
