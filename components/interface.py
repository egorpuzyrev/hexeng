#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from .component import *

from events.events import *

import json

import sfml as sf

DEFAULT_FONT = sf.Font.from_file('fonts/LiberationSans-Regular.ttf')

DEFAULT_WIDGET_DATA = {
    'isvisible': 1,
    'width': 0,
    'height': 0,
    'position': [0, 0],
    'anchor': [0, 0],
    'color': [00, 00, 00],
    'bordercolor': [00, 00, 00],
    'opacity': 255,
    'borderopacity': 255,
    'borderwidth': 2,
    'align': [0.5, 0.5],
    'font': DEFAULT_FONT,
    'font_size': 16,

    'drawable': None,
    }


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

        self.widgets_data_container.data[self.id] = {}

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
        super().update(event)
        # ~view = sf.View()
        # ~view.viewport = (0, 0, 1, 1)
        # ~oldview = self.window.view

        # ~self.window.view = view

        if event.__dict__.get('position'):
            self.intersection = self.find_intersection(event.position)
        else:
            self.intersection = {}

        width = self.window.width
        height = self.window.height
        _view = sf.View((0, 0, width, height))
        _view.viewport = (0, 0, 1.0, 1.0)
        _oldview = self.window.view
        self.window.view = _view

        for widget in self.widgets_order:
            self.widgets[widget].update(event)

        self.window.view = _oldview
        # ~supertexture = self.widgets_data_container.data[self.id]['supertexture']


    def find_intersection(self, position):

        data = self.widgets_data_container.data
        # ~widgets = [data[i]['drawable'] for i in data]

        # ~print(">>>DATA:", data)

        # ~intersection = {i: data[i]['sprite'].global_bounds.contains(position) for i in data if data[i].get('drawable')}
        intersection = [i for i in data if data[i].get('drawable') and  data[i]['sprite'].global_bounds.contains(position)]

        return intersection

class MasterWidget(Component, sf.Drawable):

    # ~def __init__(self, engineobj=None, window=None):
    def __init__(self, ifacemanager, **kwargs):
        self.engine = ifacemanager.engine
        # ~super().__init__(engineobj=self.engine)
        Component.__init__(self, engineobj=self.engine)
        sf.Drawable.__init__(self)
        
        self.manager = ifacemanager

        ifacemanager.add_widget(self, **kwargs)

# ~class Widget(Component):
class Widget(Component, sf.Drawable):

    def __init__(self, master=None, **kwargs):
        self.engine = master.engine or None
        self.id = id(self)

        Component.__init__(self, engineobj=self.engine)
        sf.Drawable.__init__(self)

        self.master = master
        self.manager = master.manager

        data = DEFAULT_WIDGET_DATA
        data.update(kwargs)

        self.manager.add_widget(self, **data)

    # ~def __enter__(self):
        # ~return self
        
    # ~def __exit__(self, type, value, traceback):
        # ~self.manager.widgets_data_container.pop(self.id)
        # ~self.manager.widgets_data_container.remove_component(self.id)

    def draw(self):
        pass

class Button(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # ~self.label = label
        widget_data = self.manager.widgets_data_container.data[self.id]

        # ~cx, cy = widget_data.get('position')  # top left corner
        cx, cy = 0, 0  # top left corner

        width, height = widget_data.get('width'), widget_data.get('height')
        bwidth = widget_data.get('borderwidth')

        align_x, align_y = widget_data.get('align')  # align of text

        cx += width*align_x + bwidth  # position of text
        # ~cy += height*align_y + bwidth  # position of text

        # ~cx += width*align_x  # position of text
        cy += height*align_y  # position of text

        # ~font = DEFAULT_FONT
        font = widget_data.get('font')  # text font

        message = widget_data.get('label')  # text itself
        # ~size = 16
        size = widget_data.get('font_size')  # font size

        pre_text = sf.Text(str(message), font, size)
        # ~pre_text.origin = (pre_text.local_bounds.width/2, pre_text.local_bounds.height/2)
        pre_text.origin = (pre_text.local_bounds.width/2, pre_text.local_bounds.height/2)
        pre_text.position = (cx, cy)

        pre_bg = sf.RectangleShape()
        pre_bg.size = (width, height)
        # ~pre_bg.origin = widget_data.get('anchor')
        pre_bg.outline_thickness = bwidth
        bordercolor = list(widget_data.get('bordercolor')) + [widget_data.get('borderopacity'),]
        pre_bg.outline_color = sf.Color(*bordercolor)
        color = list(widget_data.get('color')) + [widget_data.get('opacity'),]
        pre_bg.fill_color = sf.Color(*color)

        # ~posx, posy = widget_data.get('position')
        posx, posy = 0, 0

        pre_bg.position = (posx+bwidth, posy+bwidth)

        # ~pre = sf.RenderTexture(2000, 2000)
        # ~pre = sf.RenderTexture(width, height)
        pre = sf.RenderTexture(width+2*bwidth, height+2*bwidth)
        pre.clear(sf.Color.TRANSPARENT)
        pre.draw(pre_bg)
        pre.draw(pre_text)
        # ~pre.texture.position = (cx, cy)
        pre.display()

        widget_data['drawable'] = pre
        self.spr = widget_data['sprite'] = sf.Sprite(pre.texture)
        # ~self.spr = sf.Sprite(pre.texture)

        self.bind(UpdateSceneEvent, self.onupdate_draw)

    def onupdate_draw(self, caller, event):
        self.draw()

    def draw(self):
        
        w = self.manager.window

        widget_data = self.manager.widgets_data_container.data[self.id]

        drawable = widget_data['drawable']
        # ~w.draw(sf.Sprite(drawable.texture))

        posx, posy = widget_data['position']

        # ~x, y = posx, posy

        x, y = w.map_pixel_to_coords((posx, posy))
        # ~x, y = w.map_pixel_to_coords((0, 0))

        # ~x, y = w.map_coords_to_pixel((posx, posy))

        self.spr.position = (x, y)
        
        w.draw(self.spr)

        
    def update(self, event):
        Component.update(self, event)
        # ~self.draw()


class Label(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # ~self.label = label
        widget_data = self.manager.widgets_data_container.data[self.id]

        # ~cx, cy = widget_data.get('position')  # top left corner
        cx, cy = 0, 0  # top left corner

        width, height = widget_data.get('width'), widget_data.get('height')
        bwidth = widget_data.get('borderwidth')

        align_x, align_y = widget_data.get('align')  # align of text

        cx += width*align_x + bwidth  # position of text
        # ~cy += height*align_y + bwidth  # position of text

        # ~cx += width*align_x  # position of text
        cy += height*align_y  # position of text

        # ~font = DEFAULT_FONT
        font = widget_data.get('font')  # text font

        message = widget_data.get('label')  # text itself
        # ~size = 16
        size = widget_data.get('font_size')  # font size

        pre_text = sf.Text(str(message), font, size)
        # ~pre_text.origin = (pre_text.local_bounds.width/2, pre_text.local_bounds.height/2)
        pre_text.origin = (pre_text.local_bounds.width/2, pre_text.local_bounds.height/2)
        pre_text.position = (cx, cy)

        pre_bg = sf.RectangleShape()
        pre_bg.size = (width, height)
        # ~pre_bg.origin = widget_data.get('anchor')
        pre_bg.outline_thickness = bwidth
        bordercolor = list(widget_data.get('bordercolor')) + [widget_data.get('borderopacity'),]
        pre_bg.outline_color = sf.Color(*bordercolor)
        color = list(widget_data.get('color')) + [widget_data.get('opacity'),]
        pre_bg.fill_color = sf.Color(*color)

        # ~posx, posy = widget_data.get('position')
        posx, posy = 0, 0

        pre_bg.position = (posx+bwidth, posy+bwidth)

        # ~pre = sf.RenderTexture(2000, 2000)
        # ~pre = sf.RenderTexture(width, height)
        pre = sf.RenderTexture(width+2*bwidth, height+2*bwidth)
        pre.clear(sf.Color.TRANSPARENT)
        pre.draw(pre_bg)
        pre.draw(pre_text)
        # ~pre.texture.position = (cx, cy)
        pre.display()

        widget_data['drawable'] = pre
        self.spr = widget_data['sprite'] = sf.Sprite(pre.texture)
        # ~self.spr = sf.Sprite(pre.texture)

        self.bind(UpdateSceneEvent, self.onupdate_draw)

        self.default_view = self.manager.window.view

    def onupdate_draw(self, caller, event):

        # ~width = self.manager.window.width
        # ~height = self.manager.window.height
        # ~_view = sf.View((0, 0, width, height))
        # ~_view.viewport = (0, 0, 1.0, 1.0)
        # ~_oldview = self.manager.window.view
        # ~self.manager.window.view = _view
        # ~self.manager.window.view = self.default_view
        
        self.draw()

        # ~self.manager.window.view = _oldview

    def draw(self):
        
        w = self.manager.window

        widget_data = self.manager.widgets_data_container.data[self.id]

        drawable = widget_data['drawable']
        # ~w.draw(sf.Sprite(drawable.texture))

        posx, posy = widget_data['position']

        # ~x, y = posx, posy

        x, y = w.map_pixel_to_coords((posx, posy))
        # ~x, y = w.map_pixel_to_coords((0, 0))

        # ~x, y = w.map_coords_to_pixel((posx, posy))

        self.spr.position = (x, y)
        
        w.draw(self.spr)

        
    def update(self, event):
        Component.update(self, event)
        # ~self.draw()

class TextField(Widget):

    # ~def __init__(self, master=None, label='', position=(0, 0), size=(0, 0), anchor=(0, 0)):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

class SelectionList(Widget):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
