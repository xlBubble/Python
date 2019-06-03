#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 10:35
# @Author  : xule
# @File    : s1.py

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


d = path.dirname('.') #获取到当前文件路径
# Read the whole text.
text = open(path.join(d, 'python'),encoding="utf-8").read() #读取制作词云的文本

#设置背景图片
# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "tuntun.jpg")))
stopwords = set(STOPWORDS)
stopwords.add("said")

#背景颜色，显示最多词数，设置背景图片，字体最大值等
wc = WordCloud(background_color="white", max_words=1500, mask=alice_coloring,
               stopwords=stopwords, max_font_size=700, random_state=42)
# generate word cloud
#生成词云
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
#绘制词云图
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()

