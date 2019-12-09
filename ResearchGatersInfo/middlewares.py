# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ResearchGatersInfo.settings import MY_USER_AGENT as ua_list

class UserAgentMiddlerware(object):
    def process_request(self,request,spider):
        user_agent=random.choice(ua_list)
        request.headers['User-Agent']=user_agent
        print(request.headers['User-Agent'])

class SeleniumMiddlerware(object):
    flag=-1
    email='lipf23@mail2.sysu.edu.cn'
    #waiting for input
    password='MyliFe98!'
    url=''
    html=''

    def process_request(self,request,spider):
        self.url=request.url
        self.flag = self.flag + 1
        if(self.flag==1):
            # print("*************************************"+self.flag)
            self.driver=webdriver.Chrome()
            self.driver.get(request.url)
            time.sleep(20)

            #then have to log in
            buttonLoginOverview=self.driver.find_element_by_xpath('//a[@class="lite-page__header-link js-lite-click"]')
            buttonLoginOverview.click()
            time.sleep(10)

            inputEmail=self.driver.find_element_by_xpath('//input[@id="input-header-login"]')
            inputEmail.send_keys(self.email)
            inputPassword=self.driver.find_element_by_xpath('//input[@id="input-header-password"]')
            inputPassword.send_keys(self.password)

            buttonLoginLoginArea=self.driver.find_element_by_xpath('//div[@class="lite-page__header-login-container js-target-login"]//button[@type="submit"]')
            buttonLoginLoginArea.click()
            time.sleep(20)

            self.url=self.driver.current_url
            self.html = self.driver.page_source

            # self.flag=self.flag+1
            # response=scrapy.http.HtmlResponse(url=url,body=html,request=request,encoding='utf-8')

            # websource01=dict()
            # websource01=response.meta['websource']

        if(self.flag==2):
            buttonViewAllFollowing=self.driver.find_element_by_xpath('//div[@class="nova-o-stack nova-o-stack--gutter-xxl nova-o-stack--spacing-xxs nova-o-stack--show-divider"]/div[1]/div/div[1]//button')
            buttonViewAllFollowing.click()
            time.sleep(10)
            # js='var q=document.documentElement.scrollTop=1000'
            # self.driver.execute_script(js)
            # scrollAreaFollowing=self.driver.find_element_by_xpath('//div[@class="profile-follow-modal"][1]')
            # scrollAreaFollowing.click()
            # scrollAreaFollowing=self.driver.find_element_by_xpath('//span/div[@class="nova-c-modal nova-c-modal--color-green nova-c-modal--position-center nova-c-modal--spacing-xxl nova-c-modal--width-s is-closeable"]')
            scrollAreaFollowing = self.driver.find_element_by_xpath('//body')
            scrollAreaFollowing.send_keys(Keys.DOWN)
            time.sleep(20)
            self.html=self.driver.page_source
            #then have to shut the page down
        if (self.flag==3):
            buttonViewAllFollowers= self.driver.find_element_by_xpath('//div[@class="nova-o-stack nova-o-stack--gutter-xxl nova-o-stack--spacing-xxs nova-o-stack--show-divider"]/div[2]/div/div[1]//button')
            buttonViewAllFollowers.click()
            time.sleep(10)
            js='var q=document.documentElement.scrollTop=1000'
            self.driver.execute_script(js)
            time.sleep(20)
            self.html = self.driver.page_source
        if (self.flag==4):
            buttonViewAllForCoAuthors = self.driver.find_element_by_xpath('//div[@class="nova-c-card nova-c-card--spacing-none nova-c-card--elevation-1-above profile-top-coauthors with-top-coauthors"]/div[1]/div[1]//button')
            buttonViewAllForCoAuthors.click()
            time.sleep(10)
            js='var q=document.documentElement.scrollTop=1000'
            self.driver.execute_script(js)
            self.time.sleep(20)
            html = self.driver.page_source
        if (self.flag==5):
            #buttonInfo = self.driver.find_element_by_xpath(……)
            #buttonInfo.click()
            time.sleep(10)
            self.url = self.driver.current_url
            self.html=self.driver.page_source
        if (self.flag==6):
            # buttonScores = self.driver.find_element_by_xpath(……)
            # buttonScores.click()
            time.sleep(10)
            self.url = self.driver.current_url
            self.html = self.driver.page_source
            self.driver.quit()

            #need? then find the button to shut the view all page down--No
            # self.driver.quit()

        response=scrapy.http.HtmlResponse(url=self.url,body=self.html,request=request,encoding='utf-8')

            # response=scrapy.http.HtmlResponse(url=request.url,body=html,request=request,encoding='utf-8')
        return response
# class MyUserAgentMiddleware(UserAgentMiddleware):
#
#     def __init__(self, user_agent):
#         self.user_agent = user_agent
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             user_agent=crawler.settings.get('MY_USER_AGENT')
#         )
#
#     def process_request(self, request, spider):
#         agent = random.choice(self.user_agent)
#         request.headers['User-Agent'] = agent

# class ResearchgatersinfoSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


# class ResearchgatersinfoDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
