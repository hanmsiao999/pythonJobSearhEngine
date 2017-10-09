from django.shortcuts import render

# Create your views here.
import json
import redis
import time
import os

from django.views.generic.base import View
from django.http import HttpResponse
from pathlib import Path

from .models import es_jobType

from elasticsearch import Elasticsearch

redis_cli = redis.StrictRedis(host='182.254.155.33',password='wenyuan123')

class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s',"")
        re_datas = []
        if key_words:
            s = es_jobType.search()
            s = s.suggest('my-suggest',text=key_words,completion={
               "field":"suggest",
               "fuzzy":{
                   "fuzziness": 2,  #  单词距离
               },
               "size":10
            })
            suggestions = s.execute_suggest()
            for math in getattr(suggestions,"my-suggest")[0]['options']:
               source = math._source
               re_datas.append(source['title'])
            return HttpResponse(json.dumps(re_datas),content_type="application")


class IndexView(View):
    def get(self, request):
        topN_search = redis_cli.zrevrangebyscore("searh_keywords_set", "+inf", "-inf", start=0, num=5)
        return render(request,"index.html",{"topN_search":topN_search})


client = Elasticsearch(hosts=['127.0.0.1']) # 初始化连接
class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q","")
        s_type = request.GET.get("s_type","")

        redis_cli.zincrby("searh_keywords_set", key_words)
        topN_search = redis_cli.zrevrangebyscore("searh_keywords_set", "+inf", "-inf", start=0, num=5)
        lagouCount = redis_cli.get("lagouJobCount")
        wuyouCount = redis_cli.get("wuyouJobCount")
        jobboleCount = redis_cli.get("jobbole_count")


        if s_type == "job":
            page = int(request.GET.get("p", 1))
            begin = time.time()
            response = client.search(
                index="jobdb",
                doc_type='pythonjob',
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["title", "companyName", "jobDesc"],
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ["</span>"],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    }
                }
            )
            end = time.time()
            time_consume = round(end - begin, 5)
            total_nums = response['hits']["total"]
            page_num = int(total_nums / 10)
            hit_list = []
            for hit in response['hits']['hits']:
                hit_dict = {}
                if "highlight" in hit and "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"]["title"])
                else:
                    hit_dict["title"] = hit["_source"]["title"]

                if "highlight" in hit and "jobDesc" in hit["highlight"]:
                    hit_dict["jobDesc"] = "".join(hit["highlight"]["jobDesc"])[:500]
                else:
                    hit_dict["jobDesc"] = "".join(hit["_source"]["jobDesc"])[:500]

                # hit_dict["create_date"] = hit["_source"]["create_date"]
                hit_dict["jobCity"] = hit["_source"]["jobCity"]
                hit_dict["jobUrl"] = hit["_source"]["jobUrl"]
                hit_dict["score"] = round(hit["_score"], 3)
                hit_dict["job_org"] = hit["_source"]["job_org"]
                hit_dict['create_time'] = hit['_source']['create_time']
                hit_dict['companyName'] = hit['_source']['companyName']
                hit_list.append(hit_dict)
            return render(request, "result_job.html", {"all_hits": hit_list,
                                                   "total_nums": total_nums, "page": page, "page_num": page_num,
                                                   "time_consume": time_consume,
                                                   "key_words": key_words,
                                                   "topN_search": topN_search,
                                                   'wuyouCount': wuyouCount,
                                                   'lagouCount': lagouCount,
                                                   'jobboleCount': jobboleCount,
                                                   's_type': s_type})
        elif s_type == 'article':
            page = int(request.GET.get("p", 1))
            begin = time.time()
            response = client.search(
                index="jobdb",
                doc_type = 'article_jobdb',
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["title", "content"],
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ["</span>"],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    }
                }
            )
            end = time.time()
            time_consume = round(end - begin, 5)
            total_nums = response['hits']["total"]
            page_num = int(total_nums / 10)
            hit_list = []
            for hit in response['hits']['hits']:
                hit_dict = {}
                if "highlight" in hit and "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"]["title"])
                else:
                    hit_dict["title"] = hit["_source"]["title"]

                if "highlight" in hit and "content" in hit["highlight"]:
                    hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]
                else:
                    hit_dict["content"] = "".join(hit["_source"]["content"])[:500]


                hit_dict["url"] = hit["_source"]["url"]
                hit_dict["score"] = round(hit["_score"], 3)
                hit_dict["article_org"] = hit["_source"]["article_org"]
                hit_dict['create_date'] = hit['_source']['create_date']
                hit_list.append(hit_dict)
            return render(request, "result_article.html", {"all_hits": hit_list,
                                                   "total_nums": total_nums, "page": page, "page_num": page_num,
                                                   "time_consume": time_consume,
                                                   "key_words": key_words,
                                                   "topN_search": topN_search,
                                                   'wuyouCount': wuyouCount,
                                                   'lagouCount': lagouCount,
                                                   'jobboleCount':jobboleCount,
                                                   's_type': s_type})
        elif s_type == 'statistics':
            P = Path()
            P = P.parent / 'static' / 'img'
            files = list(P.glob("*薪资分布.jpg"))
            files = map(lambda  x:x.name,files)
            return render(request,"statistics.html",{'files':files})

