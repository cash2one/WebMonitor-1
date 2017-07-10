#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod

from interface.IPage import IPage


class BasePage(IPage):
    def __init__(self, callback, url, file_name, title):
        self.url = url
        self.date_file_name = file_name
        self.title = title
        IPage.__init__(self, callback)

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass


class BaseReqPage(BasePage):
    def __init__(self, callback, url, file_name, title, _page_req):
        self.page_req = _page_req
        BasePage.__init__(self, callback, url, file_name, title)

    def init(self):
        self.read_arts_map_file(self.date_file_name)

    def start(self):
        self.page_req.fetch(self)
        if self.new_arts:
            self.write_arts_list_file(self.new_arts, self.date_file_name)
        if self.callback:
            self.callback(str(self.title) + "#" + str(self.url), self.new_arts)
