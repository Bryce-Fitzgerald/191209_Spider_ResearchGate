import json
import csv
import scrapy
import  re

from pyasn1.compat.octets import null

from ResearchGatersInfo import items
from ResearchGatersInfo.items import ResearchgatersinfoItem


class ResearchersinfoSpider(scrapy.Spider):
    name="researchersInfo"
    # start_urls = ['https://www.researchgate.net/profile/C_Chen4']
    item = ResearchgatersinfoItem()
    # start_urls=[]
    # websource=dict()
    # start_urls = 'https://www.researchgate.net/profile/C_Chen4'
    # def start_requests(self):
    #     start_urls = ['https://www.researchgate.net/profile/C_Chen4']
    #     self.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     yield scrapy.Request(url=start_urls,callback=self.parse())
    # start_urls=['https://www.researchgate.net/profile/Zhang_Zha/info']

    # def start_requests(self):
    #     start_urls = 'https://www.researchgate.net/profile/C_Chen4'
    #     yield scrapy.Request(url=start_urls,callback=self.parse,dont_filter=True)

    def start_requests(self):
        urls = []
        with open('csvTest.csv', 'r') as f:
            reader = csv.reader(f)
            print("******************************the Reader")
            for i in reader:
                urls.append(i[1])
                print("********************************" + urls[0])
            f.close()
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        # start_urls = 'https://www.researchgate.net/profile/C_Chen4'
        print("*****************************************!!!!!!!!!!!")
        # with open('csvTest.csv','r') as f:
        #     reader=csv.reader(f)
        #     print("******************************the Reader")
        #     for i in reader:
        #         url=i[1]
        #         self.start_urls.append(url)
        #         print("********************************"+self.start_urls)
        #     for j in self.start_urls:
        #         yield scrapy.Request(url=j, callback=self.parse_overview)
        url=response.url
        print(url)
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        # websource='overview'
        yield scrapy.Request(url=url, callback=self.parse_overview,dont_filter=True)
        # nameAndInstitution=response.css('a[href*="topic"]::text').extract()
        # nameAndInstitution=response.body
        #
        # item=ResearchgatersinfoItem()
        # item['username']=response.xpath('//title')
        # item['organization']=response.xpath('//*[@class="nova-v-institution-item__stack-item"][1]//a/text()')
        # item['location']=response.xpath('//*[@class="nova-v-institution-item__stack-item"]//span/text()')
        # item['apartment']=response.xpath('//*[@class="nova-v-institution-item__stack-item"][3]//a/text()')
        # item[]
        # a="wtf"
        # filename='test03.html'
        # filename_a='test03.txt'
        # self.log("******************** %s *********************" % nameAndInstitution)
        # # with open(filename,'wb') as f:
        # #     f.write(nameAndInstitution)
        # #     f.close()
        # # with open(filename_a,'wb') as f:
        # #     f.write(a)
        # #     f.close()
        # f=open(filename,'wb+')
        # # f.write(" ".join(nameAndInstitution))
        # f.write(nameAndInstitution)
        # f.close()

    def parse_overview(self,response):
    # def parse(self,response):
        print("**************************************when I change the overview to parse only")
        # item=ResearchgatersinfoItem()
        self.item['username'] = response.xpath('//title')
        self.item['organization'] = response.xpath('//*[@class="nova-v-institution-item__stack-item"][1]//a/text()')
        self.item['location'] = response.xpath('//*[@class="nova-v-institution-item__stack-item"]//span/text()')
        self.item['apartment'] = response.xpath('//*[@class="nova-v-institution-item__stack-item"][3]//a/text()')
        self.item['totalResearchInterest']=response.xpath('//li[@class="application-box-layout__item application-box-layout__item--m"][1]/div/div/div/div/div[1]/text()')
        self.item['citations']=response.xpath('//li[@class="application-box-layout__item application-box-layout__item--m"][2]/div/div/div/div/div[1]/text()')
        self.item['recommendations']=response.xpath('//li[@class="application-box-layout__item application-box-layout__item--m"][3]/div/div/div/div/div[1]/text()')
        self.item['reads']=response.xpath('//li[@class="application-box-layout__item application-box-layout__item--m"][4]/div/div/div/div/div[1]/text()')
        #following……
        #followers……
        #topCo-authors……
        self.item['researchItems']=response.xpath('//ul[@class="application-box-layout"]/li[1]//div[@class="nova-c-card__body nova-c-card__body--spacing-inherit"]/div[1]/text()')
        self.item['project']=response.xpath('//ul[@class="application-box-layout"]/li[2]//div[@class="nova-c-card__body nova-c-card__body--spacing-inherit"]/div[1]/text()')
        self.item['questions']=response.xpath('//ul[@class="application-box-layout"]/li[3]//div[@class="nova-c-card__body nova-c-card__body--spacing-inherit"]/div[1]/text()')
        self.item['answers']=response.xpath('//ul[@class="application-box-layout"]/li[4]//div[@class="nova-c-card__body nova-c-card__body--spacing-inherit"]/div[1]/text()')
        # self.websource['view']=1
        print('**************************************************'+str(self.item)+'**************************************************')

        yield scrapy.Request(url=response.url,callback=self.parse_viewAllForFollowing,dont_filter=True)

    def parse_viewAllForFollowing(self,response):
        self.item['following']=response.xpath('//div[@class="nova-o-stack nova-o-stack--gutter-m nova-o-stack--spacing-none nova-o-stack--show-divider nova-o-stack--no-gutter-outside"]//div[@class="nova-v-person-list-item__align-content"]/div/a/text()')
        # self.websource['view'] =2
        yield scrapy.Request(url=response.url,callback=self.parse_viewAllForFollowers,dont_filter=True)

    def parse_viewAllForFollowers(self,response):
        self.item['followers']=response.xpath('//div[@class="nova-o-stack nova-o-stack--gutter-m nova-o-stack--spacing-none nova-o-stack--show-divider nova-o-stack--no-gutter-outside"]//div[@class="nova-v-person-list-item__align-content"]//a/text()')
        # self.websource['view']=3
        yield scrapy.Request(url=response.url,callback=self.parse_viewAllForCoAuthors,dont_filter=True)

    def parse_viewAllForCoAuthors(self,response):
        self.item['topCoauthors']=response.xpath('//ul[@class="nova-e-list nova-e-list--size-l nova-e-list--type-bare nova-e-list--spacing-none"]//div[@class="nova-v-person-list-item__align-content"]/div/a/text()')
        # self.websource['view']=4
        yield scrapy.Request(url=response.url,callback=self.parse_info,dont_filter=True)

    def parse_info(self,response):
        self.item['topics']=response.xpath('//div[@class="keyword-dialog-content"]//ul[@class="c-list js-widgetContainer"]/li/div/text()')
        # websource='scores'
        yield scrapy.Request(url=response.url,callback=self.parse_scores,dont_filter=True)

    def parse_scores(self,response):
        self.item['rgScoreTotal']=response.xpath('//div[@class="nova-c-card__body nova-c-card__body--spacing-inherit"]/*[2]/div[1]//div[@class="number"]/text()')
        self.item['rgScorePublications']=response.xpath('//div[@class="rg-score-breakdown"]//div[@class="legend-right"]/div[1]//span[@class="label-legend-count label-legend-percent"]//text()')
        self.item['rgScoreQuestions']=response.xpath('//div[@class="rg-score-breakdown"]//div[@class="legend-right"]/div[2]//span[@class="label-legend-count label-legend-percent"]//text()')
        self.item['rgScoreAnswers']=response.xpath('//div[@class="rg-score-breakdown"]//div[@class="legend-right"]/div[3]//span[@class="label-legend-count label-legend-percent"]//text()')
        self.item['rgScoreFollowers']=response.xpath('//div[@class="rg-score-breakdown"]//div[@class="legend-right"]/div[4]//span[@class="label-legend-count label-legend-percent"]//text()')
        self.item['rgScorePercentile']=response.xpath('//div[@class="profile-reputation-percentile"]/div[2]//span[@class="pct-arrow"]/@style')
        self.item['hIndexWithSelfcitations']=response.xpath('//div[@class="nova-l-flex__item h-index"]//div[@class="number"]/text()')
        self.item['hIndexExcludingSelfcitations']=response.xpath('//div[@class="nova-l-flex__item h-index-discounting"]//div[@class="number"]/text()')
        yield self.item