#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/8 5:09'

# 根据jobDesc 绘制词云
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from pathlib import Path
import collections, re, os
import jieba
import imageio
jieba.add_word("FullStack")
jieba.add_word("Full Stack")

path = Path(os.path.dirname(__file__)).parent / 'static' / 'img'
path = path / 'wordCount.png'


client = Elasticsearch(hosts=['127.0.0.1']) # 初始化连接
alice_coloring = imageio.imread( "alice_color.png")


s = Search(using=client,index='jobdb',doc_type='pythonjob')
s = s.source(['jobDesc'])


word_list = []
for hit in s.scan():
    text = hit['jobDesc']
    data = jieba.cut(text)
    #data = list(filter(lambda x:re.findall("[\u4e00-\u9fa5]{2,}|[A-Za-z]+",x),data))
    data = list(filter(lambda x: re.findall("[A-Za-z]+", x), data))
    word_list.extend(data)
word_freq = collections.Counter(word_list)
wc = WordCloud(background_color="white", font_path='C:/Windows/Fonts/MSYH.TTC',
               mask=alice_coloring,stopwords=STOPWORDS,max_font_size=40, random_state=42,max_words=200)
wc.generate_from_frequencies(word_freq)
image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(wc)
plt.axis("off")
plt.show()
wc.to_file(str(path))