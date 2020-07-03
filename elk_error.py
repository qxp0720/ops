# -*- coding: utf-8 -*-
from random import choice

import json
import requests
from elasticsearch import Elasticsearch


es_host = ('172.16.1.121', '172.16.1.122', '172.16.1.123')

nginx_dict = {
    '市级': 'sj-nginx',
    '市直属': 'szs-nginx',
    '园区分中心': 'yqfzx-nginx',
    '相城分中心': 'xcfzx-nginx',
    '高新区分中心': 'gxfzx-nginx',
    '昆山分中心': 'ksfzx-nginx',
    '太仓分中心': 'tcfzx-nginx',
    '姑苏分中心': 'gsfzx-nginx',
    '吴中分中心': 'wzfzx-nginx',
    '张家港分中心': 'zjgfzx-nginx',
    '常熟分中心': 'csfzx-nginx',
    '吴江分中心': 'wjfzx-nginx',
    '园区易加互动': 'sip-nginx',
    '小通优课': 'xtyk-nginx',
}

###钉钉报警
def dingding(user, text):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=69a7a866f9c80e6217c47e3b3b79ff6869191c586ce2214b1149bcad7f9d0d4d"
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