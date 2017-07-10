#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from abc import abstractmethod

import requests

from bean.article import Article
from tools.file_utils import FileUtils


class IPage:
    def __init__(self, callback):
        self._callback = callback
        self._old_arts_map = {}
        self._new_arts = []
        self._url = ''
        self._date_file_name = ''
        self._title = ''
        self.req_headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
        self.req_timeout = 10  # 3秒
        FileUtils.init_dir_path()
        self.init()
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @property
    def callback(self):
        return self._callback

    @property
    def old_arts_map(self):
        return self._old_arts_map

    @property
    def new_arts(self):
        return self._new_arts

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self._url = new_url

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def date_file_name(self):
        return self._date_file_name

    @date_file_name.setter
    def date_file_name(self, new_name):
        self._date_file_name = new_name

    def read_arts_map_file(self, file_name):
        path = FileUtils.get_data_path(file_name)
        if FileUtils.exists_path(path):
            f = file(path, "r")
            try:
                while (1):
                    line = f.readline()
                    if not line:
                        break
                    art = Article.build_article(line)
                    key_ = self.get_md5(art.link)
                    if key_:
                        self.old_arts_map[key_] = art
            except Exception, e:
                print e.args
            finally:
                f.close()

    @staticmethod
    def write_arts_list_file(list_art, file_name):
        path = FileUtils.get_data_path(file_name)
        if not FileUtils.exists_path(path):
            FileUtils.build_data_file(file_name)
        f = file(path, "a")
        try:
            for art in list_art:
                f.write(art.to_line_str())
        except Exception, e:
            print e.args
        finally:
            f.close()

    @staticmethod
    def get_md5(str_):
        return hashlib.md5(str_).hexdigest()

    def req_get(self):
        try:
            req = requests.get(self.url, headers=self.req_headers, timeout=self.req_timeout)
            if req.status_code == requests.codes.ok:
                print "req_succeed-->" + self.url
                return req.content
            else:
                print "req_failure-->" + self.url
                return None
        except Exception, e:
            print "REQ-error->" + str(e.message)
            return None
