#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

import sfml as sf
#~ from sfml import sf

# ~from engine.engine import Engine


# ~from components.components import *
from .component import *
# ~from models.models import *
from events.events import *
from support.support import *


class Renderer(Component):

    def __init__(self, engineobj=None, graphicscomponent=None, window=None):
        super().__init__(engineobj)

        self.graphics_component = graphicscomponent
        self.add_container(graphicscomponent)
        self.graphics_component_id = graphicscomponent.id

        self.window = window


    def draw_static(self, name, x1=None, y1=None, rectangle=None, anchor=None):
        """
        name - name of sprite in db
        x1, y1 - coords; if None - previous position
        """

        sprites_container = self.graphics_component.sprites_container


        # ~sprite = sprites_container.data[self.graphics_component_id]['static'][name]
        sprite = sprites_container.data[self.graphics_component_id][name]['sprite']

        width = sprite.texture.width
        height = sprite.texture.height

        if not x1 is None and not y1 is None:
            sprite.position = (x1, y1)

        if not rectangle is None:
            sprite.texture_rectangle = rectangle
            width = rectangle.width
            height = rectangle.height

        if not anchor is None:
            sprite.origin = (anchor[0]*width, anchor[1]*height)

        self.window.draw(sprite)



    def draw_sprite(self, name, x1=None, y1=None, rectangle=None, anchor=None, category='static'):
        """
        name - name of sprite in db
        x1, y1 - coords; if None - previous position
        """

        sprites_container = self.graphics_component.sprites_container


        # ~sprite = sprites_container.data[self.graphics_component_id]['static'][name]
        sprite = sprites_container.data[self.graphics_component_id][name]['sprite']

        width = sprite.texture.width
        height = sprite.texture.height

        if not x1 is None and not y1 is None:
            sprite.position = (x1, y1)

        if not rectangle is None:
            sprite.texture_rectangle = rectangle



        if not anchor is None:
            sprite.origin = (anchor[0]*width, anchor[1]*height)

        self.window.draw(sprite)


    def draw_animation(self, name, x1, y1, x2, y2, step=100, steps=0, category='animation'):
        """
        name - name of animation in db
        x1, y1 - start
        x2, y2 - finish
        step - size of dx in pixels
        speed - length of pause after each frame, in ms
        """

        sprites_container = self.graphics_component.sprites_container

        sprite = sprites_container.data[self.graphics_component_id]['animation'][name][0]
        frames = sprites_container.data[self.graphics_component_id]['animation'][name][1]

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        dx = x2 - x1
        dy = y2 - y1



        if abs(dx)>S/100:


            steps = abs(int(dx//step))
        else:


            steps = abs(int(dy//step))


        width = int(sprite.texture.width)

        framewidth = int(width//frames)

        height = int(sprite.texture.height)

        cur_x = 0

        rectangle = (cur_x, 0, cur_x+framewidth, height)

        sprite.texture_rectangle = rectangle

        for i in range(steps):



            cur_x = (cur_x+framewidth)%width

            rectangle = sf.Rectangle((cur_x, 0), (framewidth, height))




            self.engine.push_event(DrawMapEvent(layer='Surfaces'))
            self.engine.push_event(DrawMapEvent(layer='UnitsTextures'))



            self.engine.push_event(DrawStaticEvent(name=name, x1=int(x1+i*dx/steps), y1=int(y1+i*dy/steps), anchor=(0.5, 0.5), rectangle=rectangle))
            self.engine.push_event(DisplayEvent())


    def animate(self, name, x1, y1, x2, y2, step=100, steps=0):
        """
        name - name of animation in db
        x1, y1 - start
        x2, y2 - finish
        step - size of dx in pixels
        speed - length of pause after each frame, in ms
        """

        sprites_container = self.graphics_component.sprites_container

        # ~print('sprites_container.data[self.graphics_component_id].keys():', sprites_container.data[self.graphics_component_id].keys())

        sprite = sprites_container.data[self.graphics_component_id][name]['sprite']
        frames = sprites_container.data[self.graphics_component_id][name]['frames']

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        dx = x2 - x1
        dy = y2 - y1



        if abs(dx)>S/100:


            steps = abs(int(dx//step))
        else:


            steps = abs(int(dy//step))


        width = int(sprite.texture.width)

        framewidth = int(width//frames)

        height = int(sprite.texture.height)

        cur_x = 0

        rectangle = (cur_x, 0, cur_x+framewidth, height)

        sprite.texture_rectangle = rectangle

        for i in range(steps):

            cur_x = (cur_x+framewidth)%width

            rectangle = sf.Rectangle((cur_x, 0), (framewidth, height))

            # ~self.engine.push_event(DrawMapEvent(layer='Surfaces'))
            # ~self.engine.push_event(DrawMapEvent(layer='UnitsTextures'))

            self.engine.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'Buildings', 'UnitsTextures']))

            self.engine.push_event(DrawStaticEvent(name=name, x1=int(x1+i*dx/steps), y1=int(y1+i*dy/steps), anchor=(0.5, 0.5), rectangle=rectangle))
            # ~self.engine.push_event(DisplayEvent())


    def render_prerendered_map(self, layer='Surfaces'):

        mapobj = self.engine.containers['MAP']

        sprites_container = self.graphics_component.sprites_container

        sprites = sprites_container.data[self.graphics_component_id]['prerendered']

        map_texture = sprites[layer]

        sprite = sf.Sprite(map_texture.texture)


        self.window.draw(sprite)


    def draw_map_layer(self, layer='Surfaces'):

        mapobj = self.engine.containers['MAP']

        sprites_container = self.graphics_component.sprites_container

        sprites = sprites_container.data[self.graphics_component_id]['prerendered']

        map_texture = sprites[layer]

        sprite = sf.Sprite(map_texture.texture)

        self.window.draw(sprite)



    def render_map(self):

        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        sprites_container = self.graphics_component.sprites_container

        sprites = sprites_container.data[self.graphics_component_id]['static']

        surfaces_layer = [[sprites[i] for i in j] for j in mapobj.layers['Surfaces']]


        for i in enumerate(surfaces_layer):
            for j in enumerate(surfaces_layer[i[0]]):

                sprite = j[1]

                width = sprite.texture.width

                height = sprite.texture.height

                sprite.origin = (width//2, height//2)

                sprite.position = (t['hex_x'](i[0], j[0], S), t['hex_y'](i[0], j[0], S))

                self.window.draw(sprite)


