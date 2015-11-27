#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Graphics component handles loading static and animated images.
It requires special container named 'spritecontainer' to store sprites.
"""

import sys
sys.path.append('../')

from components.component import Component
from engine.engine import Engine
from models.container import Container
from models.unit import Unit
from support.support import *


import sfml as sf


class Graphics(Component):

    def __init__(self, engineobj=None, spritescontainer=None):

        super().__init__(engineobj)

        self.sprites_container = spritescontainer
        self.add_container(spritescontainer)
        self.sprites_container_id = spritescontainer.id

        self.prerendered = {}

        self.counter = 0

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {'static': {},
                             'animation': {},
                             'prerendered': {}
                            }


    def load_static(self, name, path):
        """Loads static sprites from file usable for SFML"""

        objid = self.sprites_container.id

        if not objid in self.containers:
            raise Exception("Object %s has no sudch (%s) component" %(objid, type(self)))
        else:
            data = self.containers[objid].data[self.id]

            try:
                texture = sf.Texture.from_file(path)
                data['static'][name] = sf.Sprite(texture)
            except:
                raise Exception("File %s not found or corrupted" %(path, ))

    def load_animation(self, name, path, frames=0):
        """Loads static sprites from file usable for SFML"""

        objid = self.sprites_container.id

        if not objid in self.containers:
            raise Exception("Object %s has no sudch (%s) component" %(objid, type(self)))
        else:
            data = self.containers[objid].data[self.id]

            try:
                texture = sf.Texture.from_file(path)

                if frames == 0:
                    frames = int(texture.size[0]//texture.size[1])

                data['animation'][name] = [sf.Sprite(texture), frames]
            except:
                raise Exception("File %s not found or corrupted" %(path, ))

    def bind_sprite(self, objid, name):
        """Binds static sprite to object"""

        obj = self.engine.containers[objid]
        # ~ data = obj.data

        if not objid in self.containers:
            self.add_container(obj)

        # ~ print(obj.data[self.id].keys())

        obj.data[self.id]['static'][name] = self.sprites_container.data[self.id]['static'][name]

    def bind_animation(self, objid, name):
        """Binds static sprite to object"""

        obj = self.engine.containers[objid]

        if not objid in self.containers:
            self.add_container(obj)

        obj.data[self.id]['animation'][name] = self.sprites_container.data[self.id]['animation'][name]

    def prerender_map_layer(self, layer='Surfaces'):

        data = self.sprites_container.data

        data[self.id]['prerendered']['MAP'] = sf.RenderTexture(1000, 1000)

        pre = data[self.id]['prerendered']['MAP']

        pre.clear(sf.Color.TRANSPARENT)

        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        sprites_container = self.sprites_container

        sprites = sprites_container.data[self.id]['static']

        surfaces_layer = [[sprites[i] for i in j] for j in mapobj.layers['Surfaces']]

        for i in enumerate(surfaces_layer):
            for j in enumerate(surfaces_layer[i[0]]):

                sprite = j[1]

                width = sprite.texture.width

                height = sprite.texture.height

                sprite.origin = (width//2, height//2)

                sprite.position = (t['hex_x'](j[0], i[0], 40), t['hex_y'](j[0], i[0], 40))

                pre.draw(sprite)


        font = sf.Font.from_file('/usr/share/fonts/truetype/msttcorefonts/arial.ttf')

        for i in range(mapobj.Y):
            for j in range(mapobj.X):
                # ~ text = sf.Text(str((j, i))+'\n'+str(mapobj.layers['Surfaces'][i][j]), font, 12)
                text = sf.Text(str((j, i))+'\n', font, 12)
                text.color = sf.Color.RED
                # ~ text.origin = (1.0, 1.0)
                text.position=(t['hex_x'](j, i, 40), t['hex_y'](j, i, 40))
                pre.draw(text)

        pre.display()

        # ~ self.window.display()

    def update_map_layer(self, x1=0, y1=0, tile='', layer='Surface'):

        data = self.sprites_container.data

        # ~ data[self.id]['prerendered']['MAP'] = sf.RenderTexture(1000, 1000)

        pre = data[self.id]['prerendered']['MAP']

        # ~ pre.clear(sf.Color.TRANSPARENT)

        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        sprites_container = self.sprites_container

        sprites = sprites_container.data[self.id]['static']

        # ~ surfaces_layer = [[sprites[i] for i in j] for j in mapobj.layers['Surfaces']]

        sprite = sprites[tile]

        width = sprite.texture.width

        height = sprite.texture.height

        sprite.origin = (width//2, height//2)

        sprite.position = (t['hex_x'](x1, y1, 40), t['hex_y'](x1, y1, 40))

        pre.draw(sprite)

        # ~ pre.display()


if __name__ == '__main__':

    e = Engine()

    c = Container()

    u = Unit(e)

    g = Graphics(e, c)

    g.load_static('asd', '/home/egor/Programs/win/py/hexeng/test/resources/hex40_red.png')

    g.bind_sprite(u.id, 'asd')