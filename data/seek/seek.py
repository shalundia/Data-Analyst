#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 22:57:42 2017

@author: zuoshan

A scraper to get job info form seek.com.au 
"""

import requests
from bs4 import BeautifulSoup
import json

class Seek:
    
    def __init__(self):
        self.csv_data=[]
    

    def get(self,day=1):
            url = "https://jobsearch-api.cloud.seek.com.au/search"
            header={"Accept":"application/json",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                    "Connection":"keep-alive",
                    "Host":"jobsearch-api.cloud.seek.com.au",
                    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                    }
            param ={
                    "siteKey":"AU-Main",
                    "sourcesystem":"houston",
                    "userqueryid":"249857e674883605056cd745fae88bec-6971939",
                    "userid":"6b9936ba-de09-477a-ae76-25b61a4ec8d1",
                    "usersessionid":"6b9936ba-de09-477a-ae76-25b61a4ec8d1",
                    "eventCaptureSessionId":"eb23e1b5-5b7f-42f9-b9a6-fd05e0b03a20",
                    "where":"All Sydney NSW",
                    "page":"1",
                    "seekSelectAllPages":"true",
                    "classification":"6281",
                    "daterange":"1",
                    "include":"seodata"
                    }
            param['daterange']=str(day)
            req = requests.get(url,params=param)
            print(req.status_code)
            if req.status_code==requests.codes.ok:
                data=req.json()
                total=data["totalCount"]
                pages=int(total/22)+1    
                print('total items '+str(total)+', pages '+str(pages))
                self.csv_data.extend(data["data"])
            
                for x in range(2,pages):
                    param["page"]=str(x)
                    req = requests.get(url,params=param)
                    self.csv_data.extend(req.json()["data"])
                    print('get '+str(len(self.csv_data))+' items')
            self.dump('seek_data.json')
                    
    def content(self):
        url='https://www.seek.com.au/job/'
        param={"type":"promoted",
                "userqueryid":"249857e674883605056cd745fae88bec-6971939"
            }
        for item in self.csv_data:
            print('get id='+str(item['id'])+' detail description')
            url=url+str(item["id"])
            param['type']=item['displayType']
            req = requests.get(url,params=param)
            if req.status_code==requests.codes.ok:
                soup = BeautifulSoup(req.text, 'html.parser')
                item['detailDescription']=soup.find('div',class_='templatetext').get_text()
        self.dump('seek_data_detail.json')

    def dump(self,name):
        with open(name, 'w') as f:
            json.dump(self.csv_data, f)
        
        
        
        
if __name__=="__main__":
    seek=Seek()
    seek.get()
    seek.content()
