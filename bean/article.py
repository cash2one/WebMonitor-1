#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class Article(object):
    flag = "=#@#="

    def __init__(self, title='', link=''):
        self._title = title
        self._link = link

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, new_link):
        self._link = new_link

    @staticmethod
    def build_article(line):
        art_str = line.split(Article.flag)
        return Article(art_str[0].strip('\n'), art_str[1].strip('\n'))

    def to_line_str(self):
        return str(self.title) + Article.flag + str(self.link) + "\n"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        return "Title:" + str(self._title) + "\n" + "Link:" + str(self._link)
