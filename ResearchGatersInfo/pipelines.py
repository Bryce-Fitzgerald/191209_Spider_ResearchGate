# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json

class ResearchgatersinfoPipeline(object):

    def __init__(self):
        self.f=open("csvWriteTest.csv","a",newline="")
        self.fieldnames=["username","organization","location","apartment","totalResearchInterest","citations","recommendations","reads","researchItems","project","questions","answers","following","followers","topCoauthors","topics","rgScoreTotal","rgScorePublications","rgScoreQuestions","rgScoreAnswers","rgScoreFollowers","rgScorePercentile","hIndexWithSelfcitations","hIndexExcludingSelfcitations"]
        self.writer=csv.DictWriter(f=self.f,fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # self.file=open('researchersInfo01.json','w',encoding='utf-8')
        # content=json.dumps(dict(item),ensure_ascii=False)+'\n'
        # self.file.write(content)
        # self.file.close()
        self.writer.writerow(item)
        return item

    def close(self,spider):
        self.f.close()
