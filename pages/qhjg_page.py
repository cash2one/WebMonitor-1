#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from bean.article import Article
from interface.IPage import IPage
from interface.base_page import BaseReqPage
from interface.page_request import IRequest

'''
清华经管学院
http://emba.sem.tsinghua.edu.cn/
'''


class QHJGPage(IPage):
    def init(self):
        pass

    def start(self):
        file_name = "qhjg.txt"
        # 新闻聚焦
        url_1 = "http://emba.sem.tsinghua.edu.cn/gyxm/mtjj.html"
        title_1 = "清华经管学院-新闻聚焦"
        # 活动预告
        url_2 = "http://emba.sem.tsinghua.edu.cn/hdyg.html"
        title_2 = "清华经管学院-活动预告"
        # 活动回顾
        url_3 = "http://emba.sem.tsinghua.edu.cn/xxsy/hdhg.html"
        title_3 = "清华经管学院-活动回顾"
        # 企业实践
        url_4 = "http://emba.sem.tsinghua.edu.cn/xxsy/qysj.html"
        title_4 = "清华经管学院-企业实践"
        # TODO 视频墙
        # url_5 = "http://emba.sem.tsinghua.edu.cn/kcjx/spq.html"
        # title_5 = "清华经管学院-视频墙"
        BaseReqPage(self.callback, url_1, file_name, title_1, ReqQHJGCommon).start()
        BaseReqPage(self.callback, url_2, file_name, title_2, ReqQHJGCommon).start()
        BaseReqPage(self.callback, url_3, file_name, title_3, ReqQHJGCommon).start()
        BaseReqPage(self.callback, url_4, file_name, title_4, ReqQHJGCommon).start()


class ReqQHJGCommon(IRequest):
    @staticmethod
    def fetch(page):
        try:
            print "fetch-->" + page.title
            web = page.req_get()
            if not web:
                print "req_timeout"
                return
            soup = BeautifulSoup(web, "html.parser")
            tags_div = soup.findAll('div', class_="mtgzlist mg")
            for tag in tags_div:
                if tag.a:
                    time_ = tag.findAll(class_="mtgzlistrx mg2 xi13")[0].get_text(" ", strip=True).encode("utf-8")
                    context_ = tag.findAll(class_="mtgzlistrs mg2 xi15")[0].get_text(strip=True).encode("utf-8")
                    title = context_ + time_
                    link = "http://emba.sem.tsinghua.edu.cn" + tag.a["href"].strip().encode("utf-8")
                    key_ = page.get_md5(link)
                    if key_ in page.old_arts_map.keys():
                        print "has-->" + title
                    else:
                        print "update-->" + title
                        page.old_arts_map[key_] = Article(title, link)
                        page.new_arts.append(Article(title, link))
        except Exception, e:
            print e.args
