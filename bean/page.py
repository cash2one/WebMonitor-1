#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse


class Page(object):
    def __init__(self, title='', url=''):
        self._title = title
        self._url = url

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self._url = new_url

    def get_host(self):
        u = urlparse.urlparse(self.url)
        return u[0] + "://" + u[1]

    def get_join_url(self, path):
        _path = path.encode("utf-8")
        u_ = urlparse.urlparse(_path)
        if u_.scheme == "mailto" or u_.scheme == "tel" or u_.hostname == "weibo.com" or u_.hostname == "map.baidu.com":
            return None
        else:
            return str(urlparse.urljoin(self.url, _path))

    @staticmethod
    def build_page(line):
        page_str = line.split("##")
        return Page(page_str[0].strip('\n'), page_str[1].strip('\n'))
