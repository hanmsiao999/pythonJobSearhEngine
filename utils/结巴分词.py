#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/8 6:33'


import jieba
import jieba.posseg as pseg
import jieba.analyse
import re

str3 = "职位描述：岗位职责：1.负责产品管理模块开发；2.负责产品自动集成测试工具开发；3.负责各种系统辅助功能模块；4.负责问题定位处理等。任职资格：1.本科及以上学历,计算机数学等相关专业；2.精通linux 下python开发；3.了解django/web.py/pylons/flask 框架一种及以上；4.熟悉linux系统管理；5.熟悉TCP/IP及常用网络协议，网络设备配置；6.熟悉前后端开发优先。"

#seg_list = jieba.cut(str3,cut_all = True)   ##全模式
#result = pseg.cut(str3)                     ##词性标注，标注句子分词后每个词的词性
result2 = jieba.cut(str3)                   ##默认是精准模式
#result3 =  jieba.analyse.extract_tags(str3,2)
##关键词提取，参数setence对应str1为待提取的文本,topK对应2为返回几个TF/IDF权重最大的关键词，默认值为20
#result4 = jieba.cut_for_search(str3)
result2 = list(filter(lambda x:re.findall("[\u4e00-\u9fa5]|",x),result2))
#print (list(result))
print (list(result2))
#print (list(result3))
#print (list(result4))