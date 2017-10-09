#coding:utf-8


from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text,Integer

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class es_jobType(DocType):
    # 职位类型
    title = Text(analyzer='ik_max_word')
    suggest = Completion(analyzer=ik_analyzer)
    companyName = Text(analyzer='ik_max_word')
    workAdress = Keyword()
    salary_mid = Integer
    salaryInfo = Keyword()
    jobDesc = Text(analyzer='ik_max_word')
    jobCity = Keyword()
    jobUrl = Keyword()
    job_org = Keyword()


    class Meta:
        index = "jobdb"
        doc_type = "pythonjob"


if __name__ == '__main__':
    es_jobType.init()