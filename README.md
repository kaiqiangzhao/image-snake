# imageSnake

图片贪吃蛇：由图片构成身体部分的贪吃蛇(也许不能算是个游戏)

特点：
- 食物顺序可以自定义
- 蛇头尾可以自定义
- 第一个吃的食物自定义
- 速度自定义

当初想在B站做软件测评相关的视频，缺个有创意的视频开头。

后来想到了不断的吃APP的应用的图标的贪吃蛇来做视频开头。

于是乎，就有了imageSnake。(不知道还有哪些应用场景)

你可以更换foods文件夹内的图片, 做成你想要的样子.

# demo

## 游戏开始(吃第一个食物)

![demo1](https://github.com/kaiqiangzhao/imageSnake/blob/master/static/demo/demo1.png)

## 游戏过程

![demo2](https://github.com/kaiqiangzhao/imageSnake/blob/master/static/demo/demo2.png)


# 运行

1. 创建虚拟环境

```shell
mkvirtualenv image-snake 
```

2. 安装依赖
```shell
pip install -r requirements.txt
```

3. 运行游戏
```shell
python snake.py
```

# 其它

配置(config.py)
- first_food_img可以设置为你想让贪吃蛇吃的第一个食物的图片名称
- snake_head_img是蛇头图片
- snake_tail_img是蛇尾图片
- is_order_foods是否按照图片名的顺序依次出现

# 文件说明

tools/img_round.py 图片圆角化

tools/logo_spider.py 爬取应用图标

static/weimijianshu.otf 中文字体

## 注意:

pygame不支持圆角转换图片, 可以使用tools/img_round.py对爬取的图标非圆角化
