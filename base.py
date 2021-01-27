#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from config import GameConfig


class Node:
    def __init__(self, img_path):
        self.width = GameConfig.node_width
        self.height = GameConfig.node_height
        self.image = self.init_image(img_path)

    @staticmethod
    def init_image(img_path):
        image = pygame.transform.scale(
            pygame.image.load(img_path).convert_alpha(),
            (GameConfig.node_width, GameConfig.node_height)
        )
        return image


class Point:
    def __init__(self, px: int, py: int):
        self.px = px
        self.py = py

    @property
    def pixel_x(self):
        return self.px * GameConfig.node_width

    @property
    def pixel_y(self):
        return self.py * GameConfig.node_height


class Direction(str):
    LEFT_VALUE = "left"
    RIGHT_VALUE = "right"
    UP_VALUE = "up"
    DOWN_VALUE = "down"

    def __new__(cls, value):
        return super(Direction, cls).__new__(cls, value)

    @property
    def opposite(self):
        if self == self.__class__.LEFT_VALUE:
            return self.__class__.RIGHT_VALUE
        if self == self.__class__.RIGHT_VALUE:
            return self.__class__.LEFT_VALUE
        if self == self.__class__.UP_VALUE:
            return self.__class__.DOWN_VALUE
        if self == self.__class__.DOWN_VALUE:
            return self.__class__.UP_VALUE
