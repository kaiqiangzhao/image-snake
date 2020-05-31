#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pygame.locals import *
import random
import pygame
import config


class RectAngle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Food:
    def __init__(self, shape, image):
        self.shape = shape
        self.image = image


class Cooker:
    @classmethod
    def make_food(cls):
        # 制作食物
        shape = RectAngle(50, 50)
        image_path = "icon_basket/foods/first_food.png"
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (shape.width, shape.height))
        food = Food(shape, image)
        return food

    @classmethod
    def draw_food(cls, surface, position: tuple, food, border_color=(0, 0, 0), border_width=0, border_radius=0):
        cls.draw_border(surface, position, food.shape.width, food.shape.height, border_color, border_width, border_radius)
        cls.draw_food(surface, position, food.image)

    @classmethod
    def draw_image(cls, surface, position: tuple, image):
        surface.blit(image, position)

    @classmethod
    def draw_border(cls, surface, position: tuple, width, height, border_color=(0, 0, 0), border_width=1, border_radius=0):
        pygame.draw.rect(
            surface,
            border_color,
            (
                position[0] - border_width,
                position[1] - border_width,
                width + 2 * border_width,
                height + 2 * border_width
            ),
            border_width,
            border_radius=border_radius
        )


class SnakeNode(Food):
    def __init__(self, shape, image, direction=0):
        super(SnakeNode, self).__init__(shape, image)
        self.direction = direction


class Snake:
    def __init__(self, head: SnakeNode, tails: list):
        self.head = head
        self.length = 1 + len(tails)
        self.body = tails

    def move(self, direction):
        pass

    def eat(self, food):
        pass


class Referee:
    # 裁判员
    def check_snake_out_window(self):
        # 检查是否移出窗口
        pass

    def check_snake_eat_food(self):
        # 检查是否吃到食物
        pass

    def check_snake_collide_self(self):
        # 检查是否碰撞到自己
        pass


class Game:

    def __init__(self):
        self.food_point = None
        self.snake_points = []
        self.referee = Referee()

    def rand_emtpy_point(self):
        # 寻找空白的坐标点
        pass

    def ready_start(self):
        # 开始界面
        pass

    def start(self):
        # 真正开始
        pass

    def quit(self):
        pass

    def restart(self):
        pass
