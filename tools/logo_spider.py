#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding': 'gzip, deflate, br',
        'Connection': 'Keep-Alive',
        'Host': 'www.appannie.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    ret = requests.get(url, headers=headers)
    return ret.content


def get_img(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    als1 = soup.find_all('a', class_="card_1o0ta6t")
    als2 = soup.find_all('a', class_="card_1o0ta6t-o_O-odd_7247dg")
    als1.extend(als2)
    icon_img = {}
    for a in als1:
        icon_img_url = a.img["src"]
        icon_img_name = a.div.p.get_text()
        icon_img[icon_img_url] = icon_img_name
    return icon_img


def download_img(url, name, path):
    name = name + ".png"
    full_path = os.path.join(path, name)
    ret = requests.get(url)
    with open(full_path, "wb") as f:
        f.write(ret.content)


def main():
    url = "https://www.appannie.com/cn/apps/ios/top/china/social-networking/ipad/"
    save_path = "imgs/spider"
    html = get_html(url)
    imgs = get_img(html)
    count = 0
    for img_url, img_name in imgs.items():
        count += 1
        print(count, img_name)
        download_img(img_url, img_name, save_path)


if __name__ == '__main__':
    main()
