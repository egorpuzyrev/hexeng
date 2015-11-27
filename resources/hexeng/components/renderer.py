#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

import sfml as sf

from engine.engine import Engine

from models.unit import Unit
from models.container import Container
from components.movement import Movement
from components.component import Component
from components.graphics import Graphics

from events.events import *
from support.support import *


# ~ import threading

class Renderer(Component):

    def __init__(self, engineobj=None, graphicscomponent=None, window=None):
        super().__init__(engineobj)

        self.graphics_component = graphicscomponent
        self.add_container(graphicscomponent)
        self.graphics_component_id = graphicscomponent.id

        self.window = window

    # ~ def init_storage(self, storage=None):
        # ~ if not storage:
            # ~ self.storage = Container(self.engine)


    def draw_static(self, name, x1=None, y1=None, rectangle=None, anchor=None):
        """
        name - name of sprite in db
        x1, y1 - coords; if None - previous position
        """

        sprites_container = self.graphics_component.sprites_container

        sprite = sprites_container.data[self.graphics_component_id]['static'][name]

        width = sprite.texture.width
        height = sprite.texture.height

        if not x1 is None and not y1 is None:
            sprite.position = (x1, y1)

        if not anchor is None:
            sprite.origin = (anchor[0]*width, anchor[1]*height)

        if not rectangle is None:
            sprite.texture_rectangle = rectangle

        self.window.draw(sprite)
        # ~ self.window.display()

    def draw_animation(self, name, x1, y1, x2, y2, step=100, steps=0):
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

        print('DX, DY:', dx, dy)

        if abs(dx)>0.5:
            # ~ tg = dy/dx
            steps = abs(int(dx//step))
        else:
            # ~ tg = 0
            # ~ step = 0
            steps = abs(int(dy//step))
            # ~ steps = frames

        width = sprite.texture.width

        framewidth = width//frames

        height = sprite.texture.height

        cur_x = 0

        rectangle = (cur_x, 0, cur_x+framewidth, height)

        sprite.texture_rectangle = rectangle

        # ~ sprite.position = (x1, y1)
# ~
        # ~ self.window.draw(sprite)
# ~
        # ~ self.window.display()
# ~
        # ~ sprite.position = (x1, y1)
        # ~
        # ~ self.engine.push_event(DrawEvent(name='mans3', x1=x1, y1=y1, anchor=(0.5, 0.5)))

        for i in range(steps):

            # ~ sprite.move((step, tg*step))

            cur_x = (cur_x+framewidth)%width

            # ~ rectangle = sf.Rectangle((cur_x, 0), (framewidth, height))

            # ~ sprite.texture_rectangle = rectangle

            # ~ self.engine.push_event(DrawEvent(name='bullet_anim_1', x1=x1+i*step, y1=y1+tg*i*step, anchor=(0.5, 0.5)))
            self.engine.push_event(DrawMapEvent())
            self.engine.push_event(DrawEvent(name='bullet_anim_1', x1=x1+i*dx//steps, y1=y1+i*dy//steps, anchor=(0.5, 0.5)))
            self.engine.push_event(DisplayEvent())



            # ~ self.window.draw(sprite)

            # ~ self.window.display()

            # ~ print('TAP')
            # ~ sf.sleep(sf.milliseconds(speed))


    def render_prerendered_map(self):

        mapobj = self.engine.containers['MAP']

        sprites_container = self.graphics_component.sprites_container

        sprites = sprites_container.data[self.graphics_component_id]['prerendered']

        map_texture = sprites['MAP']

        sprite = sf.Sprite(map_texture.texture)

        # ~ print('sprite.texture_rectangle:', sprite.texture_rectangle)

        self.window.draw(sprite)
        # ~ self.window.display()

    def render_map(self):

        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        # ~ print('MAPTYPE:', t)

        sprites_container = self.graphics_component.sprites_container

        sprites = sprites_container.data[self.graphics_component_id]['static']

        surfaces_layer = [[sprites[i] for i in j] for j in mapobj.layers['Surfaces']]
#        units_layer = [sprites[i] for i in mapobj.layers['Units']]
#        buildings_layer = [sprites[i] for i in mapobj.layers['Buildings']]

        for i in enumerate(surfaces_layer):
            for j in enumerate(surfaces_layer[i[0]]):

                sprite = j[1]

                width = sprite.texture.width

                height = sprite.texture.height

                sprite.origin = (width//2, height//2)

                sprite.position = (t['hex_x'](i[0], j[0], 40), t['hex_y'](i[0], j[0], 40))

                self.window.draw(sprite)



        # ~ self.window.display()




if __name__=='__main__':
    e = Engine()

    c = Container(e)

    g = Graphics(e, c)

    r = Renderer(e, g)



