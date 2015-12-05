#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from .component import *

import json

import sfml as sf


class IFaceManager(Component):

    # ~def __init__(self, engineobj=None, graphicscomponent=None, window=None):
    def __init__(self, engineobj=None, widgetsdatacontainer=None, window=None):
        print("asfsjdhflkahgkjfd")
        print("asfsjdhflkahgkjfd")
        print("asfsjdhflkahgkjfd")
        print("asfsjdhflkahgkjfd")
        print("asfsjdhflkahgkjfd")
        super().__init__(engineobj)

        # ~self.graphics_component = graphicscomponent
        # ~self.add_container(graphicscomponent)
        # ~self.graphics_component_id = graphicscomponent.id

        self.window = window

        self.widgets_order = []
        self.widgets = {}

        # ~self.widgets_data_container = Container()
        self.widgets_data_container = widgetsdatacontainer
        self.add_container(self.widgets_data_container)
        self.widgets_data_container_id = self.widgets_data_container.id

    def add_widget(self, widget, **kwargs):

        self.widgets_order.append(widget.id)
        self.widgets[widget.id] = widget

        self.widgets_data_container.data[widget.id] = kwargs

    def add_container(self, obj):
        super().add_container(obj)

        obj.data[self.id] = []
                            
    def remove_container(self, objid):
        super().remove_container(objid)

    def bind(self, event_type, handler, mode='+'):
        super().bind(event_type, handler, mode='+')
            
    def update(self, event):
        # ~super().update(event)
        for widget in self.widgets_order:
            self.widgets[widget].update(event)


class MasterWidget(Component):

    # ~def __init__(self, engineobj=None, window=None):
    def __init__(self, ifacemanager, **kwargs):
        self.engine = ifacemanager.engine
        super().__init__(engineobj=self.engine)
        
        self.manager = ifacemanager

        ifacemanager.add_widget(self, **kwargs)

# ~class Widget(Component):
class Widget(Component):

    def __init__(self, master=None, **kwargs):
        self.engine = master.engine or None
        super().__init__(engineobj=self.engine)

        self.master = master
        self.manager = master.manager

        self.manager.add_widget(self, **kwargs)

class Button(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # ~self.label = label

class Label(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # ~self.label = label

class TextField(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # ~self.label = label

class SelectionList(Widget):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
