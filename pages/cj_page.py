#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 长江商学院
from bs4 import BeautifulSoup

from bean.article import Article
from interface.IPage import IPage
from interface.base_page import BaseReqPage
from interface.page_request import IRequest

'''
长江商学院
http://www.ckgsb.edu.cn/emba/
'''


# 新闻
# http://www.ckgsb.edu.cn/emba/article

# 活动预告
# http://www.ckgsb.edu.cn/emba/activity

# 校友故事
# http://www.ckgsb.edu.cn/emba/story

# TODO 视频
# http://www.ckgsb.edu.cn/about/video/82

class CJPage(IPage):
    def init(self):
        pass

    def start(self):
        file_name = "cj.txt"
        # 新闻
        url_1 = "http://www.ckgsb.edu.cn/emba/article"
        title_1 = "长江商学院-新闻"
        # 活动预告
        url_2 = "http://www.ckgsb.edu.cn/emba/activity"
        title_2 = "长江商学院-活动预告"
        # 校友故事
        url_3 = "http://www.ckgsb.edu.cn/emba/story"
        title_3 = "长江商学院-校友故事"
        BaseReqPage(self.callback, url_1, file_name, title_1, ReqCJCommon).start()
        BaseReqPage(self.callback, url_2, file_name, title_2, ReqCJCommon).start()
        BaseReqPage(self.callback, url_3, file_name, title_3, ReqCJStory).start()


class ReqCJCommon(IRequest):
    @staticmethod
    def fetch(page):
        try:
            print "fetch-->" + page.title
            web = page.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_li = soup.findAll('li', class_="clearfix")
            for tag in tags_li:
                if tag.a:
                    time_ = tag.findAll(class_="date_act")[0].get_text(" ", strip=True).encode("utf-8")
                    context_ = tag.findAll(class_="act_center_tit")[0].get_text(strip=True).encode("utf-8")
                    title = time_ + context_
                    link = "http://www.ckgsb.edu.cn" + tag.a["href"].strip().encode("utf-8")
                    key_ = page.get_md5(link)
                    if key_ in page.old_arts_map.keys():
                        print "has-->" + title
                    else:
                        print "update-->" + title
                        page.old_arts_map[key_] = Article(title, link)
                        page.new_arts.append(Article(title, link))
        except Exception, e:
            print e.args


class ReqCJStory(IRequest):
    @staticmethod
    def fetch(page):
        try:
            print "fetch-->" + page.title
            web = page.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_li = soup.findAll('li', class_="clearfix")
            for tag in tags_li:
                if tag.a:
                    time_ = tag.findAll(class_="time_line_r")[0].get_text(" ", strip=True).encode("utf-8")
                    context_ = tag.findAll("h6")[0].get_text(strip=True).encode("utf-8")
                    title = time_ + context_
                    link = "http://www.ckgsb.edu.cn" + tag["onclick"].split("'")[1].strip().encode("utf-8")
                    key_ = page.get_md5(link)
                    if key_ in page.old_arts_map.keys():
                        print "has-->" + title
                    else:
                        print "update-->" + title
                        page.old_arts_map[key_] = Article(title, link)
                        page.new_arts.append(Article(title, link))
        except Exception, e:
            print e.args
