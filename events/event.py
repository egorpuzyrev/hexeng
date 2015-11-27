#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class Event(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)