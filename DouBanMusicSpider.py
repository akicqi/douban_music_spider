#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
一个简单的Python爬虫, 用于抓取豆瓣音乐Top250的名称
Anthor: AkiC
Date: 2015-06-14
"""
import string
import urllib2
from bs4 import BeautifulSoup

class DouBanMusicSpider(object) :
    """类的简要说明
    本类主要用于抓取豆瓣前250的音乐名称(使用BeautifulSoup改进解析)
    
    params:
        page: 用于表示当前所处的抓取页面
        cur_url: 用于表示当前争取抓取页面的url
        datas: 存储处理好的抓取到的音乐名称
        _top_num: 用于记录当前的top号码
    """
    def __init__(self) :
        self.page = 1
        self.cur_url = "http://music.douban.com/top250?start={page}"
        self.datas = []
        self._top_num = 1
        print u"豆瓣音乐爬虫准备就绪, 准备爬取Top250音乐数据..."
    def get_page(self, cur_page) :
        """
        根据当前页码爬取网页HTML
        Args: 
            cur_page: 表示当前所抓取的网站页码
        Returns:
            返回抓取到整个页面的HTML(unicode编码)
        Raises:
            URLError:url引发的异常
        """
        url = self.cur_url
        try :
            #每页有25条记录
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8","ignore")
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page
    def find_title(self, my_page) :
        """
        通过返回的整个网页HTML, 正则匹配前250的音乐名称
        Args:
            my_page: 传入页面的HTML文本用于正则匹配
        """
        temp_data = []
        soup = BeautifulSoup(my_page)
        #用BeautifulSoup查找类nbg，取得数据
        data = soup.find_all(class_="nbg")
        for item in data:
            #数据追加进temp_data列表
            temp_data.append("Top" + str(self._top_num) + " " + item['title'])
            self._top_num += 1
        self.datas.extend(temp_data)
    
    def start_spider(self) :
        """
        爬虫入口, 并控制爬虫抓取页面的范围
        """
        while self.page <= 10 :
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1
def main() :
    print u"""
        ###############################
            一个简单的豆瓣音乐前250爬虫
            Author: AkiC
            Date: 2015-06-14
        ###############################
    """
    my_spider = DouBanMusicSpider()
    my_spider.start_spider()
    for item in my_spider.datas :
        print item
    print u"豆瓣爬虫爬取结束..."
if __name__ == '__main__':
    main()