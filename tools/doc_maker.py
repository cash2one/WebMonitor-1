#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class DocMaker(object):
    m_html = '''<html>
    <head><meta charset="UTF-8"><title>{}</title></head>
    <body>{}</body>
    </html>'''

    @staticmethod
    def maker_mail_context(data_map):
        loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        title = "<h1>%s 更新内容:</h1>"
        text = [title % str(loc_time)]
        for key in data_map:
            key_ = key.split("#")
            text.append('''<h2>[PAGE]:Begin##############<a href="%s">%s</a>################</h2>''' % (
                str(key_[1]), str(key_[0])))
            for date in data_map[key]:
                text.append('''<p><a href="%s">%s</a></p>''' % (str(date.link), str(date.title)))
            text.append("<h2>[PAGE]:END##############%s##################</h2>" % str(key_[0]))
        return "".join(text)

    @staticmethod
    def maker_html_context(data_map):
        loc_time = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime())
        title = "<h1>{} 更新内容:</h1>".format(str(loc_time))
        text = [title]
        for key in data_map:
            key_ = key.split("#")
            text.append('''<h2>[PAGE]:Begin##############<a href="%s">%s</a>################</h2>''' % (
                str(key_[1]), str(key_[0])))
            for date in data_map[key]:
                text.append('''<p><a href="%s">%s</a></p>''' % (str(date.link), str(date.title)))
            text.append("<h2>[PAGE]:END##############%s##################</h2>" % str(key_[0]))
        return {"date": str(loc_time), "doc": DocMaker.m_html.format(str(loc_time), str("".join(text)))}
