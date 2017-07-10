#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interface.IPage import IPage
from pages.bjjt_page import BJJTPage
from pages.cj_page import CJPage
from pages.default_page import DefaultPage
from pages.guanghua_page import GHPage
from pages.qhjg_page import QHJGPage


class PageEngine(IPage):
    def start(self):
        # 光华学院
        GHPage(self.callback).start()
        # 北京交通
        BJJTPage(self.callback).start()
        # 长江学院
        CJPage(self.callback).start()
        # 清华经管
        QHJGPage(self.callback).start()
        # default
        DefaultPage(self.callback).start()

    def init(self):
        print "init page engine"
