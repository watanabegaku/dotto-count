# -*- coding: utf-8 -*-
"""ブロックの数計測.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KAZ1_nq0a4KsSCtp_2l02j3w7fE26hG0
"""

pip install opencv-python numpy

import cv2
import numpy as np

def count_color_blocks(image, color_ranges, window_size=(200, 100)):
    # 画像を読み込む
    image = cv2.imread(image)
    if image is None:
        print("画像が読み込めませんでした。")
        return

    # RGBからHSVへ変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    height, width, _ = image.shape
    results = []

    # 画像を指定したウィンドウサイズで分割
    for y in range(0, height, window_size[1]):
        for x in range(0, width, window_size[0]):
            window = hsv[y:y+window_size[1], x:x+window_size[0]]
            color_counts = {}

            # 各色のブロック数をカウント
            for color, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(window, lower, upper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                color_counts[color] = len(contours)

            results.append(((x, y), color_counts))

    return results

# 色の範囲をHSVで定義
COLOR_RANGES = {
    'red': ((0, 70, 50), (10, 255, 255)),
    'blue': ((110, 50, 50), (130, 255, 255)),
    'gray': ((0, 0, 50), (180, 15, 255))
}

# 画像パスを指定
image_path = '/content/スクリーンショット 2024-05-26 091014.png'

# ブロックを検出
results = count_color_blocks(image_path, COLOR_RANGES)

# 結果を表示
for position, color_counts in results:
    print(f"位置 {position}:")
    for color, count in color_counts.items():
        print(f"  {color} ブロック数: {count}")