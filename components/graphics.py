#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Graphics component handles loading static and animated images.
It requires special container named 'spritecontainer' to store sprites.
"""

import sys
sys.path.append('../')

# ~from components.components import *
from .component import *

from models.models import *
# ~from engine.engine import Engine

# ~from support.support import *

import sfml as sf
#~ from sfml import sf


class Graphics(Component):

    def __init__(self, engineobj=None, spritescontainer=None):

        super().__init__(engineobj)

        self.sprites_container = spritescontainer
        self.add_container(spritescontainer)
        self.sprites_container_id = spritescontainer.id


        self.counter = 0

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {'static': {},
                             'animation': {},
                             'prerendered': {}
                            }


    def load_texture(self, name, path, **kwargs):
        """Loads static sprites from file usable for SFML"""

        objid = self.sprites_container.id

        if not objid in self.containers:
            raise Exception("Object %s has no such (%s) component" %(objid, type(self)))
        else:
            data = self.containers[objid].data[self.id]

            try:
                texture = sf.Texture.from_file(path)
                data[name] = {}
                data[name]['sprite'] = sf.Sprite(texture)

                if not 'frames' in kwargs:
                    frames = int(texture.size[0]//texture.size[1])

                data[name]['frames'] = frames

            except:
                raise Exception("File %s not found or corrupted" %(path, ))

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

    def bind_sprite(self, objid, name, name1=''):
        """Binds static sprite to object"""

        obj = self.engine.containers[objid]


        if not objid in self.containers:
            self.add_container(obj)

        if name1=='':
            name1 = name

        obj.data[self.id][name1] = {}
        obj.data[self.id][name1]['sprite'] = self.sprites_container.data[self.id][name]
        obj.data[self.id][name1]['original_name'] = name

    def bind_animation(self, objid, name, name1=''):
        """Binds static sprite to object"""



        obj = self.engine.containers[objid]

        if not objid in self.containers:
            self.add_container(obj)

        if name1=='':
            name1 = name

        obj.data[self.id]['animation'][name1] = self.sprites_container.data[self.id]['animation'][name]

    def prerender_map_layer(self, layer='Surfaces'):

        data = self.sprites_container.data

        X = self.engine.containers['MAP'].X
        Y = self.engine.containers['MAP'].Y

        t = self.engine.containers['MAP'].type

        data[self.id]['prerendered'][layer] = sf.RenderTexture(t['hex_x'](X+1, Y+1, S), t['hex_y'](X+1, Y+1, S))

        pre = data[self.id]['prerendered'][layer]

        pre.clear(sf.Color.TRANSPARENT)

        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        sprites_container = self.sprites_container

        sprites = sprites_container.data[self.id]


        for i in enumerate(mapobj.layers[layer]):
            for j in enumerate(mapobj.layers[layer][i[0]]):
                # ~print(j[1])
                # ~print(sprites)
                if j[1] in sprites:

                    sprite = sprites[j[1]]['sprite']

                    width = sprite.texture.width

                    height = sprite.texture.height

                    sprite.origin = (width//2, height//2)

                    sprite.position = (t['hex_x'](j[0], i[0], S), t['hex_y'](j[0], i[0], S))

                    pre.draw(sprite)


                elif j[1] in self.engine.containers:

                    sprite = self.engine.containers[j[1]].data[self.id]

                    width = sprite.texture.width

                    height = sprite.texture.height

                    sprite.origin = (width//2, height//2)

                    sprite.position = (t['hex_x'](j[0], i[0], S), t['hex_y'](j[0], i[0], S))

                    pre.draw(sprite)

        pre.display()

    def update_map_layer(self, x1=0, y1=0, texture='', layer='Surfaces'):

        data = self.sprites_container.data



        pre = data[self.id]['prerendered'][layer]



        mapobj = self.engine.containers['MAP']

        t = mapobj.type

        sprites_container = self.sprites_container

        sprites = sprites_container.data[self.id] # ['static']



        sprite = sprites[texture]['sprite']

        width = sprite.texture.width

        height = sprite.texture.height

        sprite.origin = (width//2, height//2)

        sprite.position = (t['hex_x'](x1, y1, S), t['hex_y'](x1, y1, S))

        pre.draw(sprite)

        pre.display()


if __name__ == '__main__':

    e = Engine()

    c = Container()

    u = Unit(e)

    g = Graphics(e, c)

    g.load_static('asd', '/home/egor/Programs/win/py/hexeng/test/resources/hex40_red.png')

    g.bind_sprite(u.id, 'asd')
