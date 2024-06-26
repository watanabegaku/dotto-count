# -*- coding: utf-8 -*-
"""ブロックの数計測.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KAZ1_nq0a4KsSCtp_2l02j3w7fE26hG0
"""

pip install opencv-python numpy

import cv2
import numpy as np

def count_color_markers(image_path, color_ranges, window_size=(176, 128)):
    # 画像を読み込む
    image = cv2.imread(image_path)
    if image is None:
        return "画像が読み込めませんでした。"

    # RGBからHSVへ変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    height, width, _ = image.shape
    results = []

    # 画像を指定したウィンドウサイズで分割
    for y in range(0, height, window_size[1]):
        for x in range(0, width, window_size[0]):
            window = hsv[y:y + window_size[1], x:x + window_size[0]]
            color_counts = {}

            # 各色のブロック数をカウント
            for color, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(window, lower, upper)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                color_counts[color] = len(contours)

            results.append(((x, y), color_counts))

    return results

# 色の範囲をHSVで定義
COLOR_RANGES = {
    'red': ((0, 120, 70), (10, 255, 255)),  # 赤色のHSV範囲
    'blue': ((100, 150, 50), (140, 255, 255)),  # 青色のHSV範囲
    'light_gray': ((0, 0, 200), (180, 30, 255))  # 明るい灰色のHSV範囲
}

# 画像パスを指定
image_path = '/content/スクリーンショット 2024-05-26 091014.png'

# ブロックを検出
results = count_color_markers(image_path, COLOR_RANGES)

# 結果を表示
for position, color_counts in results:
    print(f"位置 {position}:")
    for color, count in color_counts.items():
        print(f"  {color} マーカー数: {count}")