#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *
from random import randint
import pygame
import config


class Food:
    def __init__(self, x, y):
        # 初始化食物的位置
        self.x = x
        self.y = y

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Snake:
    def __init__(self, length=3, direction=0, step=50):
        """
        length: 初始长度
        direction: 初始方向
        step: 一步走多少个像素
        """
        self.x = []
        self.y = []
        self.step = step
        self.length = length
        self.direction = direction

        # 初始化
        for i in range(length-1, -1, -1):
            self.x.append(i * step)
            self.y.append(0)

    def update(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 0:
            self.x[0] = self.x[0] + self.step
        if self.direction == 1:
            self.x[0] = self.x[0] - self.step
        if self.direction == 2:
            self.y[0] = self.y[0] - self.step
        if self.direction == 3:
            self.y[0] = self.y[0] + self.step

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    def __init__(self):
        self.window_width = config.WINDOW_WIDTH
        self.window_height = config.WINDOW_HEIGHT
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._food_surf = None
        self.snake = Snake(length=config.SNAKE_INIT_LEN)
        rand_x, rand_y = self.rand_food_position()
        self.food = Food(rand_x, rand_y)

    def rand_food_position(self):
        # TODO: 保证食物不会出现在蛇身体上
        rand_x = randint(0, self.window_width - config.FOOD_SIZE[0])
        rand_y = randint(0, self.window_height - config.FOOD_SIZE[1])
        return rand_x, rand_y

    def is_collision_self(self, x1, y1, x2, y2):
        # 是否碰撞到自己
        # 如何判断两个矩形是否相交
        snake_width, snake_height = config.SNAKE_NODE_SIZE
        head_x_line = (x1, x1 + snake_width)
        head_y_line = (y1, y1 + snake_height)
        body_x_line = (x2, x2 + snake_width)
        body_y_line = (y2, y2 + snake_height)
        max_x_line = max(head_x_line[0], body_x_line[0])
        min_x_line = min(head_x_line[1], body_x_line[1])
        max_y_line = max(head_y_line[0], body_y_line[0])
        min_y_line = min(head_y_line[1], body_y_line[1])
        if max_x_line < min_x_line and max_y_line < min_y_line:
            return True
        else:
            return False

    def is_collision_food(self, x1, y1, x2, y2):
        # 是否碰撞到食物
        food_width, food_height = config.FOOD_SIZE
        snake_width, snake_height = config.SNAKE_NODE_SIZE
        head_x_line = (x1, x1 + snake_width)
        head_y_line = (y1, y1 + snake_height)
        food_x_line = (x2, x2 + food_width)
        food_y_line = (y2, y2 + food_height)
        max_x_line = max(head_x_line[0], food_x_line[0])
        min_x_line = min(head_x_line[1], food_x_line[1])
        max_y_line = max(head_y_line[0], food_y_line[0])
        min_y_line = min(head_y_line[1], food_y_line[1])
        if max_x_line < min_x_line and max_y_line < min_y_line:
            return True
        else:
            return False

    def is_collision_win(self, x1, y1):
        # 是否碰撞到墙壁
        if 0 <= x1 <= self.window_width and 0 <= y1 <= self.window_height:
            return False
        return True

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)
        pygame.display.set_caption("Icon Snake")

        self._running = True
        self._image_surf = pygame.transform.scale(
            pygame.image.load("./icon_basket/block.png").convert(),
            config.SNAKE_NODE_SIZE
        )
        self._food_surf = pygame.transform.scale(
            pygame.image.load("./icon_basket/food.png").convert(),
            config.FOOD_SIZE,
        )

    def on_loop(self):
        self.snake.update()

        if self.is_collision_win(self.snake.x[0], self.snake.y[0]):
            print("You lose! Collision: ")
            print(self.snake.x[0], self.snake.y[0])
            exit(0)

        for i in range(2, self.snake.length):
            if self.is_collision_self(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.snake.x[0]) + "," + str(self.snake.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.snake.x[i]) + "," + str(self.snake.y[i]) + ")")
                exit(0)

        # 把食物当成蛇的一部分进行碰撞检测
        if self.is_collision_food(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.x, self.food.y = self.rand_food_position()
            self.snake.length = self.snake.length + 1
            self.snake.x.append(0)
            self.snake.y.append(0)

    def on_render(self):
        self._display_surf.fill(config.BACKGROUND)  # 背景
        self.snake.draw(self._display_surf, self._image_surf)
        self.food.draw(self._display_surf, self._food_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        clock = pygame.time.Clock()
        while self._running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.on_cleanup()  # 接收到退出事件后，退出程序
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT and self.snake.direction != 1:  # 不能倒着走
                        self.snake.move_right()
                    elif event.key == K_LEFT and self.snake.direction != 0:
                        self.snake.move_left()
                    elif event.key == K_UP and self.snake.direction != 3:
                        self.snake.move_up()
                    elif event.key == K_DOWN and self.snake.direction != 2:
                        self.snake.move_down()
                    elif event.key == K_ESCAPE:
                        self._running = False
            self.on_loop()
            self.on_render()
            frame_rate = clock.tick(5)  # 帧率, 也对于蛇的移动速度
        self.on_cleanup()

    def start(self):
        self.on_init()
        font = pygame.font.SysFont("arial", 50)
        tip = font.render('Start Icon Snake Game!!!', True, (255, 255, 255))
        self._display_surf.blit(tip, ((self.window_width-tip.get_width())/2, (self.window_height-tip.get_height())/2))
        pygame.display.update()
        clock = pygame.time.Clock()

        while True:  # 键盘监听事件
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    self.on_cleanup()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # 终止程序
                        self.on_cleanup()  # 终止程序
                    else:
                        self.on_execute()
            frame_rate = clock.tick(10)  # 帧率,


if __name__ == "__main__":
    game = Game()
    game.start()
