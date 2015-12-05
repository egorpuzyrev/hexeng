#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from .container import Container

from support.support import *


class MasterWidget(Container):

    # ~def __init__(self, engineobj=None, selfid=None, maptype='', sizex=0, sizey=0, *layers, **components):
    def __init__(self, engineobj=None, *components):
        super().__init__(engineobj, *components)


class Widget(Container):

    # ~def __init__(self, engineobj=None, selfid=None, maptype='', sizex=0, sizey=0, *layers, **components):
    def __init__(self, master=None):
        engineobj = master.engine if master else None
        components = []
        super().__init__(engineobj, *components)

class Button(Widget):

    def __init__(self, master=None, label=''):
        super().__init__(master)
        self.widget_type = 'Button'
        self.label = label

class Label(Widget):

    def __init__(self, master=None, label=''):
        super().__init__(master)
        self.label = label

