#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageDraw

# 参考链接:https://blog.csdn.net/qilei2010/article/details/104572847


def circle_corner(img, radii):
    # 矩形图像转为圆角矩形
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形

    # 原图转为带有alpha通道（表示透明程度）
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)  # 与img同大小的白色矩形，L 表示黑白图
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见

    return img


if __name__ == '__main__':
    radii = 50
    imgs_path = "icon_basket/spider"
    for root, dirs, files in os.walk(imgs_path):
        for file in files:
            save_path = "./icon_basket/foods"
            if file.find(".png") != -1:
                print(file)
                full_path = os.path.join(root, file)
                save_path = os.path.join(save_path, file)
                img = Image.open(full_path)
                img = circle_corner(img, radii)
                img.save(save_path, 'png', quality=100)
