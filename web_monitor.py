#!/usr/bin/python
# -*- coding: UTF-8 -*-
import copy
import time

from pages.page_engine import PageEngine
from tools.doc_maker import DocMaker
from tools.file_utils import FileUtils
from tools.mail_sender import SenderMail


class Monitor:
    def __init__(self):
        self.pageIndex = 1
        self.new_date = {}

    def start(self):
        # print "start"
        PageEngine(self.date_update).start()
        time.sleep(2)
        # self.send_email()
        self.write_file()
        print "finished..."
        time.sleep(5)

    def date_update(self, key, date):
        # print "date_update-->" + key
        if date:
            self.new_date[key] = copy.deepcopy(date)

    def send_email(self):
        if not self.new_date:
            print unicode("没有更新数据", "utf8")
            return
        SenderMail().send(DocMaker.maker_mail_context(self.new_date))

    def write_file(self):
        if not self.new_date:
            print unicode("没有更新数据", "utf8")
            return
        html = DocMaker.maker_html_context(self.new_date)
        FileUtils.write_out_file(html["doc"], html["date"] + ".html")


webMonitor = Monitor()
webMonitor.start()
