#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/8 8:13'

import collections,os
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


path = Path(os.path.dirname(__file__)).parent / 'static' / 'img'
path = path / 'Python Job Distribution.jpg'



client = Elasticsearch(hosts=['127.0.0.1'])
s = Search(using=client,index='jobdb',doc_type='pythonjob')
s = s.source(['jobCity'])



jobCity = []
for hit in s.scan():
    city =  hit['jobCity'].split("-")[0]
    jobCity.append(city)

jobCity_dict = collections.Counter(jobCity)
newJobDict = {}
newJobDict['其他'] = 0
for item in jobCity_dict:
    if jobCity_dict[item]>=1000:
        newJobDict[item] = jobCity_dict[item]
    else:
        newJobDict['其他'] += jobCity_dict[item]



def make_pie_char(newJobDict):
    newJobItems = newJobDict.items()
    #for item in newJobItems:
    labels,quant= list(zip(*newJobItems))
    labels = list(labels)
    explode = [0] * len(labels)
    explode[labels.index("上海")] = 0.1
    for i in range(len(labels)):
        labels[i] = labels[i] + "(%s)" % (str(quant[i]))
    print (labels)
    plt.figure(1, figsize=(10, 10))
    plt.pie(quant,labels=labels,explode=explode, autopct='%1.1f%%', pctdistance=0.8, shadow=True)
    plt.title('Python工作分布', bbox={'facecolor': '0.8', 'pad': 5})
    #plt.show()
    plt.savefig(str(path))


make_pie_char(newJobDict)


#
# for item in (response['hits']['hits']):
#     text = item['_source']['jobCity']
#     text = text.split("-")[0]
#     jobCity.append(text)
#
# jobCity_dict = collections.Counter(jobCity)
# for item in jobCity_dict:
#     print (item,jobCity_dict[item])