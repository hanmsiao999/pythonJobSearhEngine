#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/8 4:29'

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

text = open(path.join(d, 'alice.txt')).read()
alice_coloring = imread(path.join(d, "alice_color.png"))

wc = WordCloud(background_color="white", mask=alice_coloring,stopwords=STOPWORDS.add("said"),max_font_size=40, random_state=42)
wc.generate(text)
image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(wc)
plt.axis("off")
# plt.figure()
# plt.imshow(wc.recolor(color_func=image_colors))
# plt.axis("off")
# plt.figure()
# plt.imshow(alice_coloring, cmap=plt.cm.gray)
# plt.axis("off")
plt.show()