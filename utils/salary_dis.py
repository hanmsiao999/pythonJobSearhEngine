#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/8 10:11'

import re, os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


def plot_salary(city=""):
    if not city:
        city = '全国'
    client = Elasticsearch(hosts=['127.0.0.1']) # 初始化连接
    s = Search(using=client, index='jobdb', doc_type='pythonjob')
    if city !='全国':
        s = s.query("term",jobCity=city)
    s = s.source(['salaryInfo','jobCity','jobUrl'])
    whole_salary = [0] * 1000
    url_set = set()
    for hit in s.scan():
        if hit['jobUrl'] in url_set:
            continue
        url_set.add(hit['jobUrl'])
        city = hit['jobCity']
        salary = hit['salaryInfo']
        salaryNum = map(float, re.findall("(\d+(?:\.\d+)?)", salary))
        if '年' in salary:
            salaryNum = map(lambda x: x / 12, salaryNum)
        if "万" in salary:
            salaryNum = map(lambda x:x*10,salaryNum)
        salaryNum = map(int, salaryNum)
        salaryNum = list(salaryNum)

        if len(salaryNum) == 2:
           for i in range(salaryNum[0],salaryNum[1]+1):
               try:
                  whole_salary[i]+=1
               except Exception as ex:
                   print (hit['jobUrl'])
                   print (salaryNum[1])
                   print ("="*20)

    labels = ['1-5K','6-10K','11-15K','16-20K','21-25K','26-30K','30K以上']
    dis_salary = []
    for i in range(1,31,5):
        dis_salary.append(sum(whole_salary[i:i+5]))

    dis_salary.append(sum(whole_salary[30:]))
    plt.figure(1, figsize=(10, 10))
    plt.bar(range(1, len(labels)+1), dis_salary, fc='b')
    plt.xticks(range(1, len(labels)+1), labels)
    title = 'Python%s薪资分布' % city
    plt.title(title, bbox={'facecolor': '0.8', 'pad': 5})
    plt.xlabel('薪资')
    plt.ylabel('职位数量')
    path = Path(os.path.dirname(__file__)).parent / 'static' / 'img'
    path = path / ('%s.jpg' % title)
    plt.savefig(str(path))
    plt.close('all')




#plot_salary("无锡")
#plot_salary("上海")
#plot_salary("南京")
#plot_salary("苏州")
#plot_salary("杭州")
#plot_salary("深圳")
#plot_salary("北京")
hot_city = ['无锡','上海','南京','苏州','杭州','深圳','北京']
for city in hot_city:
    plot_salary(city)

