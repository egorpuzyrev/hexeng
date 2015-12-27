#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import sys
sys.path.append('../')

from events.event import Event


class Event(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class UpdateSceneEvent(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

class DrawStaticEvent(Event):

    # ~def __init__(self, x1=None, y1=None, rectangle=None, anchor=None, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DrawTextureEvent(Event):

    # ~def __init__(self, x1=None, y1=None, rectangle=None, anchor=None, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DrawMapEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ClearCanvasEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ClearSceneEvent(Event):

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


class UpdateMapLayerEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PrerenderMapLayerEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShowHealthEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ShowMessageEvent(Event):

    def __init__(self, **kwargs):
        super()._
        _init__(**kwargs)

class AskEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OutlineUnitEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShowPossibleWaysEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CalculatePossibleWaysEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShowWayEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AIUpdateEvent(Event):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
