# -*- coding: utf-8 -*-
from random import choice

import json
import requests
from elasticsearch import Elasticsearch


es_host = ('172.16.1.121', '172.16.1.122', '172.16.1.123')

nginx_dict = {
    'sj': 'sj-nginx',
    'szs': 'szs-nginx',

}

###钉钉报警
def dingding(user, text):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token="
    data = {
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
    x = requests.post(url=webhook, data=json.dumps(data), headers=headers)

##query_nginx_error
def query_nginx(index_name, es_host, name, port=9200):
    es = Elasticsearch([{'host': es_host, 'port': port}])
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
    res = es.search(index=index_name+"-*", body=q)
    number = (res['hits']['total'])
    v = number.get('value')
    if v > 50:
        msg = name+'-nginx error number is %d' % (v)
        dingding('bzt', msg)
        # print(msg)
    else:
        pass

for k, v in nginx_dict.items():
    print(k, v)
    query_nginx(v, choice(es_host), k)
