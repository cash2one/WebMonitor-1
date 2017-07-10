#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup

from bean.article import Article
from interface.IPage import IPage


class GHPage(IPage):
    def start(self):
        GHBulletinPage(self.callback).start()
        GHNewsPage(self.callback).start()
        GHPeoplePage(self.callback).start()

    def init(self):
        print "init GH page"


"""
光华快报模块
"""


class GHBulletinPage(IPage):
    def init(self):
        # print "init GH"
        self.date_file_name = "gh.txt"
        self.url = "http://www.gsm.pku.edu.cn/emba/P26004431340948453579.html"
        self.title = "光华-快报"
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.fetch_date()
        if self.new_arts:
            # print "写数据"
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        self.callback(str(self.title) + "#" + str(self.url), self.new_arts)

    def fetch_date(self):
        try:
            print "fetch-->" + self.title
            web = self.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_a = soup.findAll(name='a', attrs={'href': re.compile("^javascript:goToInfoDetail\(")})
            for tag_a in tags_a:
                if tag_a.text and tag_a.text.strip():
                    link = self.url + "?clipperUrl=" + tag_a['href'].split("'")[1]
                    title = tag_a.text.encode("utf-8")
                    key_ = self.get_md5(link)
                    if key_ in self.old_arts_map.keys():
                        print "has-->" + str(title)
                    else:
                        print "update-->" + str(title)
                        self.old_arts_map[key_] = Article(title, link)
                        self.new_arts.append(Article(title, link))
        except Exception, e:
            print "GH-Error-->" + str(e.message)


'''
光华新闻模块
'''


class GHNewsPage(IPage):
    def init(self):
        # print "init GH"
        self.title = "光华-新闻"
        self.date_file_name = "gh.txt"
        self.url = "http://www.gsm.pku.edu.cn/emba/P26003431340948445932.html"
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.fetch_date()
        if self.new_arts:
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        self.callback(str(self.title) + "#" + str(self.url), self.new_arts)

    def fetch_date(self):
        try:
            print "fetch-->" + str(self.title)
            web = self.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_li = soup.findAll('li', 'nrjt01')
            for tag in tags_li:
                title = tag.get_text(":", strip=True).encode("utf-8")
                link = tag.a['href'].strip().encode("utf-8")
                key_ = self.get_md5(link)
                if key_ in self.old_arts_map.keys():
                    print "has-->" + title
                else:
                    print "update-->" + title
                    self.old_arts_map[key_] = Article(title, link)
                    self.new_arts.append(Article(title, link))
        except Exception, e:
            print "GH-Error-->" + str(e.message)


"""
光华人物模块
"""


class GHPeoplePage(IPage):
    def init(self):
        self.title = "光华-人物"
        self.date_file_name = "gh.txt"
        self.url = "http://www.gsm.pku.edu.cn/emba/P8801259901368692959652.html"
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.fetch_date()
        if self.new_arts:
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        self.callback(str(self.title) + "#" + str(self.url), self.new_arts)

    def fetch_date(self):
        try:
            print "fetch-->" + self.title
            web = self.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_li = soup.findAll('li', 'nrjt01')
            for tag in tags_li:
                title = tag.get_text(":", strip=True).encode("utf-8")
                link_ = tag.a['href'].strip().split("'")[1].encode("utf-8")
                link = self.url + "?clipperUrl=" + link_
                key_ = self.get_md5(link)
                if key_ in self.old_arts_map.keys():
                    print "has-->" + title
                else:
                    print "update-->" + title
                    self.old_arts_map[key_] = Article(title, link)
                    self.new_arts.append(Article(title, link))
        except Exception, e:
            print "GH-Error-->" + str(e.message)
