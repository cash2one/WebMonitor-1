#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod


class IRequest:
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def fetch(page):
        pass
