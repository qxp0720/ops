# -*- coding: utf-8 -*-
import urllib,json,sys,os,datetime
from elasticsearch import Elasticsearch
import json
###钉钉报警
def dingding(user,text):
    webhook=""
    data={
      "msgtype": "text",
      "text": {
        "content": text
     },
     "at": {
        "atMobiles": [
            user
        ],
        "isAtAll": False
     }
     }
    headers = {'Content-Type': 'application/json'}
    x=urllib.Request(url=webhook,data=json.dumps(data),headers=headers)

##wzfzx_nginx
def wzfzx_nginx():
     es = Elasticsearch([{'host': '172.16.1.121', 'port': 9200}])
     q = {"query": {
     "bool": {
        "must": {
            "bool": {
                "must": [
                    {"match": {"message": "error"}}
                ]
            }
        },
        "filter": {"range": {"@timestamp": {"gte": "now-120m"}}}
     }
     }
     }
     res = es.search(index="wzfzx-nginx-*", body=q)
     number = (res['hits']['total'])
     v=number.get('value')
     if v>0:
         msg='吴中分中心-nginx error number is %d' % (v)
         dingding('bzt',msg)
     else:
        pass
    
    
wzfzx_nginx()