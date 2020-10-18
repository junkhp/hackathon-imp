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
    # 30パーセントずつ余白を追加
    blank_size_width = int(img_width * 0.3)
    blank_size_height = int(img_height * 0.3)

    # 縦方向の余白
    black_blank_height = np.zeros((blank_size_height, img_width, 3)).astype(np.uint8)
    original_combined_image = cv2.vconcat([black_blank_height, input_image, black_blank_height])

    # 横方向の余白
    black_blank_width = np.zeros((2*blank_size_height + img_height,
                                  blank_size_width, 3)).astype(np.uint8)
    original_combined_path = get_add_path(input_image_path, 'blank_original')
    original_combined_image = cv2.hconcat(
        [black_blank_width, original_combined_image, black_blank_width])
    cv2.imwrite(original_combined_path, original_combined_image)

    # マスクを描画
    filled_image = make_masked_image(input_image, mask_points)
    cv2.imwrite(get_add_path(input_image_path, 'filled'), filled_image)

    # リサイズ
    # resize_width = int(img_width * resize_ratio)
    # resize_height = int(img_height * resize_ratio)
    # resized_input_image = cv2.resize(filled_image, (resize_width, resize_height))
    # resized_input_image_path = get_add_path(input_image_path, 'resized')
    # cv2.imwrite(resized_input_image_path, resized_input_image)

    # 縦方向の余白
    # black_blank_height = np.zeros((blank_size_height, img_width, 3)).astype(np.uint8)
    print('black_blank_heightのサイズ')
    print(black_blank_height.shape)
    print('画像のサイズ')
    print(input_image.shape)
    combined_image = cv2.vconcat([black_blank_height, filled_image, black_blank_height])

    # 横方向の余白
    # black_blank_width = np.zeros((2*blank_size_height + img_height,
    #                               blank_size_width, 3)).astype(np.uint8)
    print('black_blank_widthのサイズ')
    print(black_blank_height.shape)
    print('結合画像のサイズ')
    print(combined_image.shape)
    combined_image = cv2.hconcat([black_blank_width, combined_image, black_blank_width])
    cv2.imwrite(get_add_path(input_image_path, 'combined'), combined_image)
    # print('combined_imageのサイズ')
    # print(combined_image.shape)

    # クロップ
    left_x = mask_points[7][0]
    right_x = mask_points[1][0]
    bottom_y = mask_points[4][1]

    print('左')
    print(left_x)
    print('右')
    print(right_x)

    extended_left_x = int(left_x - input_image_distance_yoko * 0.35)
    extended_right_x = int(right_x + input_image_distance_yoko * 0.35)
    extended_bottom_y = int(bottom_y + input_image_distance_yoko * 0.05)
    extended_key_points = [extended_left_x, extended_right_x, extended_bottom_y]

    merged_extended_left_x = extended_left_x + blank_size_width
    merged_extended_right_x = extended_right_x + blank_size_width
    merged_extended_bottom_y = extended_bottom_y + blank_size_height
    merged_extended_key_points = [merged_extended_left_x,
                                  merged_extended_right_x, merged_extended_bottom_y]

    crop_size = merged_extended_right_x - merged_extended_left_x
    top_left_x = merged_extended_left_x
    top_left_y = merged_extended_bottom_y - crop_size

    merge_top_left = [top_left_x, top_left_y]

    print('クロップ画像のサイズ')
    print(crop_size)
    print(top_left_x)
    print(top_left_y)

    print('クロップするときの左上')
    print([top_left_x, top_left_y])

    cropped_image = combined_image[top_left_y: top_left_y +
                                   crop_size, top_left_x: top_left_x + crop_size]

    cropped_path = get_add_path(input_image_path, 'cropped')

    print('クロップ画像のサイズ')
    print(cropped_image.shape)

    # リサイズ
    resized_image = cv2.resize(cropped_image, (256, 256), interpolation=cv2.INTER_LANCZOS4)
    print('出力画像のサイズ')
    print(resized_image.shape)
    # 画像を保存

    cv2.imwrite(masked_image_path, resized_image)
    crop_params_dict = {
        'input_image_path': input_image_path,
        'blank_original_path': original_combined_path,
        'crop_top_left': merge_top_left,
        'original_top_left': (blank_size_width, blank_size_height),
        'cropped_size': crop_size,
        'original_image_size': (img_width, img_height),
    }
    print(crop_params_dict)

    return masked_image_path, crop_params_dict


def generate_result_image(image_path, inpainted_image_path, crop_params_dict):
    final_result_path = get_add_path(image_path, 'final_result')
    back_image = cv2.imread(crop_params_dict['blank_original_path'])
    inpainted_image = cv2.imread(inpainted_image_path)
    crop_size = crop_params_dict['cropped_size']
    original_image_size = crop_params_dict['original_image_size']
    original_top_left = crop_params_dict['original_top_left']
    resized_inpainted_image = cv2.resize(
        inpainted_image, (crop_size, crop_size), interpolation=cv2.INTER_LANCZOS4)
    # print('背景画像のサイズ')
    # print(back_image.shape)
    crop_top_left = crop_params_dict['crop_top_left']
    print('crop_top_left')
    print(crop_top_left)
    back_image[crop_top_left[1]: crop_top_left[1] + crop_size,
               crop_top_left[0]: crop_top_left[0] + crop_size] = resized_inpainted_image

    cv2.imwrite(final_result_path, back_image)

    '''背景画像をリサイズしないやり方'''
    # ToDo:リサイズのアルゴリズムの検討
    # inpainted_image_resized = cv2.resize(inpainted_image, (int(img_size), int(img_size)))

    # print('リサイズ後のインペイント画像のサイズ')
    # print(inpainted_image_resized.shape)

    print('originaltopleft')
    print(original_top_left)
    print(original_image_size)
    final_reslut_image = back_image[original_top_left[1]: original_top_left[1] +
                                    original_image_size[1], original_top_left[0]: original_top_left[0] + original_image_size[0]]
    cv2.imwrite(final_result_path, final_reslut_image)

    # '''背景画像をリサイズするやり方'''

    # print('インペイント画像のサイズ')
    # print(inpainted_image.shape)
    # print('インペイント画像の左上')
    # print(top_left)
    # print('インペイントの右下')
    # bottom_right = [top_left[0]+256, top_left[1]+256]
    # print(bottom_right)
    # print('小さい背景画像サイズ')
    # print(resized_back_image.shape)

    # if top_left[0] < 0 or top_left[1] < 0 or bottom_right[0] >= resized_back_image.shape[1] or bottom_right[1] >= resized_back_image.shape[0]:
    #     cv2.imwrite(final_result_path, inpainted_image)
    # else:
    #     resized_back_image[int(top_left[1]): int(top_left[1]) + 256,
    #                        int(top_left[0]): int(top_left[0]) + 256] = inpainted_image

    #     cv2.imwrite(final_result_path, resized_back_image)

    return final_result_path
    # return inpainted_image_pa

# if __name__ == "__main__":
#     # generate_masked_image(0, 0)
#     print(get_add_path('/kjfd/oshoi/fhido/junki.jpeg', 'mask'))
