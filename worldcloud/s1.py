#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 10:35
# @Author  : xule
# @File    : s1.py

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sys
import jieba
# Read the whole text.
text = 'Building prefix dict from the default dictionary ...'   #读取制作词云的文本
cut_text = ' '.join(jieba.lcut(text))
print(cut_text)
color_mask = imread("D:\\WorkDoc\\python\\test\\temp\\spider\\tuntun.jpg")
cloud = WordCloud(
    font_path='D:\\WorkDoc\\python\\test\\temp\\spider\\方正喵呜体.ttf', # 字体最好放在与脚本相同的目录下，而且必须设置
    background_color='white',
    mask=color_mask,
    max_words=2000,
    max_font_size=50000
)

word_cloud = cloud.generate(cut_text)
print("11")
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
