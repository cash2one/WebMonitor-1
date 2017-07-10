#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from bean.article import Article
from interface.IPage import IPage
from interface.base_page import BasePage

'''
北京交通大学经济管理学院
http://sem.bjtu.edu.cn/emba/
'''


class BJJTPage(IPage):
    def init(self):
        pass

    def start(self):
        # 项目新闻
        file_name = "bjjt.txt"
        url_1 = "http://sem.bjtu.edu.cn/emba/lists-emba_xmxw1.html"
        title_1 = "北京交通-项目新闻"
        # 项目招生动态
        url_2 = "http://sem.bjtu.edu.cn/emba/lists-emba_zsdt.html"
        title_2 = "北京交通-招生动态"
        # 高端视线
        url_3 = "http://sem.bjtu.edu.cn/emba/lists-emba_gdsx.html"
        title_3 = "北京交通-高端视线"
        # 通知公告
        url_4 = "http://sem.bjtu.edu.cn/emba/lists-emba_tzgg.html"
        title_4 = "北京交通-通知公告"
        # 通知公告
        url_5 = "http://sem.bjtu.edu.cn/emba/lists-emba_hdyg.html"
        title_5 = "北京交通-活动预告"
        BJJTBasePage(self.callback, url_1, file_name, title_1).start()
        BJJTBasePage(self.callback, url_2, file_name, title_2).start()
        BJJTBasePage(self.callback, url_3, file_name, title_3).start()
        BJJTBasePage(self.callback, url_4, file_name, title_4).start()
        BJJThdygPage(self.callback, url_5, file_name, title_5).start()


class BJJTBasePage(BasePage):
    def init(self):
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.fetch_date()
        if self.new_arts:
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        if self.callback:
            self.callback(str(self.title) + "#" + str(self.url), self.new_arts)

    def fetch_date(self):
        try:
            print "fetch-->" + self.title
            web = self.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_li = soup.findAll('ul', class_="index-news lst-news")[0].findAll('li')
            for tag in tags_li:
                if tag.a:
                    title = tag.get_text(strip=True).encode("utf-8")
                    link = tag.a["href"].strip().encode("utf-8")
                    key_ = self.get_md5(link)
                    if key_ in self.old_arts_map.keys():
                        print "has-->" + title
                    else:
                        print "update-->" + title
                        self.old_arts_map[key_] = Article(title, link)
                        self.new_arts.append(Article(title, link))
        except Exception, e:
            print e.args


class BJJThdygPage(BasePage):
    def init(self):
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.fetch_date()
        if self.new_arts:
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        if self.callback:
            self.callback(str(self.title) + "#" + str(self.url), self.new_arts)

    def fetch_date(self):
        try:
            print "fetch-->" + self.title
            web = self.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_dt = soup.findAll('dt')
            for tag in tags_dt:
                if tag.a:
                    title = tag.a["title"].strip().encode("utf-8")
                    link = tag.a["href"].strip().encode("utf-8")
                    key_ = self.get_md5(link)
                    if key_ in self.old_arts_map.keys():
                        print "has-->" + str(title)
                    else:
                        print "update-->" + str(title)
                        self.old_arts_map[key_] = Article(title, link)
                        self.new_arts.append(Article(title, link))
        except Exception, e:
            print e.args
