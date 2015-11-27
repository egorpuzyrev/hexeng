#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import sys
sys.path.append('../')

from events.event import Event


class Event(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

class DrawEvent(Event):

    # ~ def __init__(self, x1=None, y1=None, rectangle=None, anchor=None, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DrawTextureEvent(Event):

    # ~ def __init__(self, x1=None, y1=None, rectangle=None, anchor=None, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DrawMapEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ClearCanvasEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DisplayEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CloseEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EnumerateEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

