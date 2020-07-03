# -*- coding: utf-8 -*-
# @Time    : 2020-05-20
# @Author  : qiuxingping
# @FileName: DLQ_delete.py


from selenium import webdriver

amq_host=[
    '10.19.2.10',
    '10.19.2.23',
    '10.32.1.110',
    '10.32.1.123',
    '172.16.0.172',
    '172.16.0.169',
    '10.53.240.123',
    '10.53.240.115',
    '172.16.100.227',
    '172.16.100.195',
    '192.168.0.207',
    '192.168.0.208',
    '10.1.168.25',
    '10.1.168.33',
    '10.150.4.33',
    '10.150.4.25',
    '172.16.104.16',
    '172.16.104.15',
    '10.255.22.23',
    '10.255.22.15',
    '172.16.1.173',
    '172.16.1.172'
]

browers = webdriver.Chrome()

for host in amq_host:
        try:
            browers.get('http://admin:admin@%s:8161/admin/queues.jsp' %host)
            t = browers.find_element_by_xpath("//*[@id='queues']/tbody/tr[1]/td[1]")
            if t.text=="ActiveMQ.DLQ":
                d=browers.find_element_by_xpath("//*[@id='queues']/tbody/tr[1]/td[7]")
                browers.find_element_by_link_text("Delete").click()
        except Exception as e:
          print(e)
browers.quit()
         