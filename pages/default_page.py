#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup

from bean.article import Article
from bean.page import Page
from interface.IPage import IPage
from tools.file_utils import FileUtils


class DefaultPage(IPage):
    def __init__(self, callback):
        self.urls = {}
        self.filter_set = set()
        self.filter_contains_set = set()
        self.build_filter_set()
        IPage.__init__(self, callback)

    def init(self):
        self.read_urls()
        for date_ in self.urls.keys():
            FileUtils.build_data_file(date_)

    def start(self):
        for date_file in self.urls.keys():
            # 清空数据
            self.old_arts_map.clear()
            del self.new_arts[:]
            # 读取数据
            self.read_arts_map_file(date_file)
            # 获取在线数据
            page = self.urls[date_file]
            self.fetch(page)
            # 回调更新
            if self.new_arts:
                self.write_arts_list_file(self.new_arts, date_file)
                if self.callback:
                    self.callback(str(page.title) + "#" + str(page.url), self.new_arts)

    def fetch(self, page):
        self.url = page.url
        web = self.req_get()
        if not web:
            print "req_timeout"
            return
        soup = BeautifulSoup(web, "html.parser")
        tags_a = soup.find_all('a', href=True)
        for tag in tags_a:
            uri_ = tag['href'].strip()
            if not self.is_valid_url(uri_):
                print "invalid url-->" + uri_
                continue
            link = page.get_join_url(uri_)
            if link:
                key_ = self.get_md5(link)
                if key_ in self.old_arts_map.keys():
                    print "has-->" + link
                else:
                    print "update-->" + link
                    self.old_arts_map[key_] = Article(link, link)
                    self.new_arts.append(Article(link, link))

    def read_urls(self):
        path = os.getcwd() + os.sep + "urls.txt"
        if os.path.exists(path):
            f = file(path, "rU")
            try:
                while (1):
                    line = f.readline()
                    if not line:
                        break
                    line = line.replace('\r\n', '\n').replace('\r', '\n').strip('\n').strip()
                    if len(line) == 0:
                        continue
                    print "-->" + str(line)
                    p = Page.build_page(line)
                    key_ = self.get_md5(p.url)
                    if key_:
                        self.urls[key_] = p
            except Exception, e:
                print e.args
            finally:
                f.close()
        else:
            print "%s file does not exist!!!" % str(path)

    def is_valid_url(self, _url):
        if not _url:
            return False
        for _filter in self.filter_contains_set:
            if _filter in _url:
                return False
        if _url in self.filter_set:
            return False
        return True

    def build_filter_set(self):
        self.filter_contains_set.add("javascript")
        self.filter_contains_set.add("C:\Users")
        self.filter_contains_set.add("mp.weixin.qq.com")
        self.filter_contains_set.add("http://emba.dhu.edu.cn/content/show/")
        self.filter_set.add("#")
        self.filter_set.add("###")
        self.filter_set.add("/")
        self.filter_set.add("this")
        self.filter_set.add("none")
        self.filter_set.add("#left")
        self.filter_set.add("#top")
        self.filter_set.add("#right")
