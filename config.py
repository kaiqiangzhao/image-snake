#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GameConfig:
    # 窗口
    win_width = 800
    win_height = 600
    win_bg_color = (255, 255, 255)

    # 游戏
    game_logo = "static/logo.png"
    game_name = "Image Snake"
    game_font_path = "static/weimijianshu.otf"
    game_font_color = (0, 0, 0)

    # 结点
    node_width = 50
    node_height = 50
    node_border_width = 1
    node_border_color = (214, 214, 214)
    node_border_radius = 9

    # 蛇
    snake_head_img = "imgs/head.png"
    snake_tail_img = "imgs/tail.png"
    snake_move_speed = 10  # 越大越快

    # 食物
    first_food_img = "imgs/first_food.png"
    food_imgs = "imgs/foods"  # 图片文件
    is_order_food = True  # 是否按名称排序图片
