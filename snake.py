#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import pygame
from base import Node, Point, Direction
from config import GameConfig


class Food:
    def __init__(self, node: Node, point: Point):
        self.node = node
        self.point = point

    def to_snake_node(self):
        return SnakeNode(node=self.node, point=self.point)


class SnakeNode:
    def __init__(self, node: Node, point: Point):
        self.node = node
        self.point = point


class Snake:
    def __init__(self):
        self.head = None
        self.tail = None
        self.stomach = []
        self.body = []
        self.direction = Direction("right")

    def set_head(self, node: Node, point: Point):
        node.image = pygame.transform.rotate(node.image, -90)
        self.head = SnakeNode(node=node, point=point)

    def set_tail(self, node: Node, point: Point):
        self.tail = SnakeNode(node=node, point=point)

    def to_list(self):
        nodes = [self.head]
        nodes.extend(self.body)
        nodes.append(self.tail)
        return nodes

    def move(self, direction: Direction):
        if direction == self.direction or direction.opposite == self.direction:
            return True

        clockwise = [("up", "right"), ("left", "up"), ("down", "left"), ("right", "down")]

        if (self.direction, direction) in clockwise:
            turn_angle = -90
        else:
            turn_angle = 90

        self.head.node.image = pygame.transform.rotate(self.head.node.image, turn_angle)
        self.direction = direction
        return True

    def forward(self):
        self._forward_tail()
        self._forward_body()
        self._forward_head()

    def _forward_head(self):
        if self.direction == "left":
            self.head.point.px = self.head.point.px - 1
        elif self.direction == "right":
            self.head.point.px = self.head.point.px + 1
        elif self.direction == "up":
            self.head.point.py = self.head.point.py - 1
        elif self.direction == "down":
            self.head.point.py = self.head.point.py + 1

    def _forward_body(self):
        if self.stomach:  # 胃部有食物, 尾部不动, 食物追加到身体末尾
            food = self.stomach.pop()
            snake_node = food.to_snake_node()
            self.body.append(snake_node)

        if self.body:
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].point.px = self.body[i-1].point.px
                self.body[i].point.py = self.body[i-1].point.py
            self.body[0].point.px = self.head.point.px
            self.body[0].point.py = self.head.point.py

    def _forward_tail(self):
        if self.stomach:
            return None  # 胃部有食物尾部不动
        if self.body:
            self.tail.point.px = self.body[-1].point.px
            self.tail.point.py = self.body[-1].point.py
        else:
            self.tail.point.px = self.head.point.px
            self.tail.point.py = self.head.point.py

    def eat(self, food):
        self.stomach.append(food)


class GamePainter:
    # 画家
    @classmethod
    def draw_food(cls, surface, food: Food):
        cls.draw_node(surface=surface, node=food.node, point=food.point)

    @classmethod
    def draw_snake(cls, surface, snake: Snake):
        for snode in snake.to_list():
            cls.draw_node(surface=surface, node=snode.node, point=snode.point)

    @classmethod
    def draw_node(cls, surface, node, point):
        pygame.draw.rect(
            surface,
            GameConfig.node_border_color,
            (
                point.pixel_x - GameConfig.node_border_width,
                point.pixel_y - GameConfig.node_border_width,
                GameConfig.node_width + 2 * GameConfig.node_border_width,
                GameConfig.node_height + 2 * GameConfig.node_border_width
            ),
            GameConfig.node_border_width,
            border_radius=GameConfig.node_border_radius
        )
        surface.blit(node.image, (point.pixel_x, point.pixel_y))


class GameJudge:
    # 裁判员

    @classmethod
    def is_collide_food(cls, head, food):
        # 是否碰撞到食物
        if head.point.px == food.point.px and head.point.py == food.point.py:
            return True
        else:
            return False

    @classmethod
    def is_collide_self(cls, snake):
        # 和食物碰撞检测是相同的逻辑, 食物即是身体部分
        for node in snake.to_list()[1:]:
            if cls.is_collide_food(snake.head, node):
                return True
        return False

    @classmethod
    def is_collide_edge(cls, head):
        # 是否碰撞到墙壁
        is_collide = True
        if 0 <= head.point.pixel_x + GameConfig.node_width/2 <= GameConfig.win_width \
                and 0 <= head.point.pixel_y + GameConfig.node_height/2 <= GameConfig.win_height:
            is_collide = False
        return is_collide


class Game:
    def __init__(self):
        self.display_surf = self.init_window()
        self.snake = None
        self.food = None
        self.running = True
        self.table_cols = GameConfig.win_width // GameConfig.node_width - 1
        self.table_rows = GameConfig.win_height // GameConfig.node_height - 1
        self.points = set([Point(px, py) for px in range(self.table_cols+1) for py in range(self.table_rows+1)])
        self.food_images = self.get_food_imgs()

    def get_food_imgs(self):
        image_names = os.listdir(GameConfig.food_imgs)
        image_paths = [os.path.join(GameConfig.food_imgs, name) for name in image_names]
        if GameConfig.is_order_food:
            image_paths.sort()
        else:
            random.shuffle(image_paths)
        return image_paths

    @staticmethod
    def init_window():
        pygame.init()
        display_surf = pygame.display.set_mode(
            (GameConfig.win_width, GameConfig.win_height), 0, 32
        )
        display_surf.fill(GameConfig.win_bg_color)  # 背景

        logo_surf = pygame.image.load(GameConfig.game_logo).convert_alpha()
        pygame.display.set_icon(logo_surf)
        pygame.display.set_caption(GameConfig.game_name)
        return display_surf

    def init_snake(self):
        # 左上方开始
        snake = Snake()
        head_node = Node(img_path=GameConfig.snake_head_img)
        tail_node = Node(img_path=GameConfig.snake_tail_img)
        head_point = Point(1, 0)
        tail_point = Point(0, 0)
        snake.set_head(node=head_node, point=head_point)
        snake.set_tail(node=tail_node, point=tail_point)
        self.snake = snake

    def init_first_food(self):
        food_img = Node(img_path=GameConfig.first_food_img)
        point = self.find_point()
        food = Food(node=food_img, point=point)
        self.food = food

    def reset_food(self):
        if self.food_images:
            food_img_path = self.food_images.pop()
            food_img = Node(img_path=food_img_path)
        else:
            self.food_images = self.get_food_imgs()  # 重新吃所有图片
            food_img_path = self.food_images.pop()
            food_img = Node(img_path=food_img_path)
        point = self.find_point()
        food = Food(node=food_img, point=point)
        self.food = food

    def find_point(self):
        snake_nodes = self.snake.to_list() if self.snake else []
        snake_points = set([node.point for node in snake_nodes])
        empty_points = self.points - snake_points
        rand_point = random.choice(list(empty_points))
        return rand_point

    def run(self):
        self.show_start_tip()
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:  # 任意键开始
                    if self.running:
                        self.start()
                    else:
                        self.restart()

    def start(self):
        if self.running:
            self.init_snake()
            self.init_first_food()
            GamePainter.draw_snake(surface=self.display_surf, snake=self.snake)
            GamePainter.draw_food(surface=self.display_surf, food=self.food)
            pygame.display.flip()

        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  # 不能倒着走
                        self.snake.move(Direction("right"))
                    elif event.key == pygame.K_LEFT:
                        self.snake.move(Direction("left"))
                    elif event.key == pygame.K_UP:
                        self.snake.move(Direction("up"))
                    elif event.key == pygame.K_DOWN:
                        self.snake.move(Direction("down"))
            self.loop()
            clock.tick(GameConfig.snake_move_speed)  # 帧率, 也对于蛇的移动速度

    def restart(self):
        self.running = True
        self.start()

    def loop(self):
        self.display_surf.fill(GameConfig.win_bg_color)
        self.snake.forward()
        GamePainter.draw_snake(surface=self.display_surf, snake=self.snake)
        GamePainter.draw_food(surface=self.display_surf, food=self.food)
        pygame.display.update()
        if GameJudge.is_collide_self(self.snake) or GameJudge.is_collide_edge(self.snake.head):
            self.stop()
        if GameJudge.is_collide_food(self.snake.head, self.food):
            self.snake.eat(self.food)
            self.reset_food()

    def stop(self):
        self.running = False

    @staticmethod
    def quit():
        pygame.quit()

    def show_start_tip(self):
        font = pygame.font.Font(
            GameConfig.game_font_path, GameConfig.win_width // 16
        )
        tip = font.render('按任意键开始 Icon Snake!!!', True, GameConfig.game_font_color)
        self.display_surf.blit(
            tip,
            (
                (GameConfig.win_width - tip.get_width()) / 2,
                (GameConfig.win_height - tip.get_height()) / 2
            )
        )


if __name__ == '__main__':
    game = Game()
    game.run()
