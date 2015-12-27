#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
sys.path.append('../')


from components.movement import Movement
from components.attributes import Attributes
from components.graphics import Graphics
from components.ai import AI
from components.conversation import Conversation
from models.unit import Unit

from events.events import *

from .support import *

import sfml as sf

def load_map_from_file(m, g, path):

    path = resource_path(path)

    with open(path) as f:
        s = f.read()
        f.close()

    j = json.loads(s)

    print(">>>MAP TYPE:", j['type'])
    # ~print(locals())
    # ~m.type = globals().get(j['type'])
    m.type = MAP_TYPES.get(j['type'])
    print(">>>MAP SIZE:", j['size'])
    m.X, m.Y = j['size']
    layers = j['layers']
    layers_order = j['layers_order']

    print("LAYERS_ORDER:", layers_order)

    for i in layers_order:
        m.add_layer(i)
        m.set_layer(i, layers[i])

def load_textures_from_file(g, path):

    path = resource_path(path)

    with open(path) as f:
        s = f.read()
        f.close()

    j = json.loads(s)

    tileset = j['tileset']

    for i in tileset:
        g.load_texture(i, tileset[i]['path'])

def create_units_by_map(e):

    m = e.containers['MAP']
    g = e.components[Graphics]
    mov = e.components[Movement]
    a = e.components[Attributes]
    ai = e.components[AI]

    for i in enumerate(m.layers['Units']):
        for j in enumerate(i[1]):
            if not type(j[1]) is int:

                u = Unit(e)
                e.add_container(u)
                print(j)
                if 'Graphics' in j[1]:
                    u.add_component(g)
                    for k in j[1]['Graphics']:
                        g.bind_sprite(u.id, j[1]['Graphics'][k], k)

                if 'Attributes' in j[1]:
                    u.add_component(a)
                    for k in j[1]['Attributes']:
                        a.add_attribute(u.id, k)
                        a.set_attribute(u.id, k, j[1]['Attributes'][k])

                if 'Movement' in j[1]:
                    u.add_component(mov)
                    mov.set_coords(u.id, j[1]['Movement']['x'], j[1]['Movement']['y'])
                
                if 'AI' in j[1]:
                    u.add_component(ai)

                m.layers['Units'][i[0]][j[0]] = u.id
                print('NEW UNIT:', u.id, i[0], j[0])


def load_level(engine, textures_js_path=None, map_js_path=None, conversations_js_path=None):

    if textures_js_path:
        g = engine.components[Graphics]
        load_textures_from_file(g, textures_js_path)

    if map_js_path:
        m = engine.containers['MAP']
        load_map_from_file(m, g, map_js_path)
        print(">>MAP TYPE:", m.type)
        create_units_by_map(engine)
        engine.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'Buildings', 'UnitsTextures']))

    if conversations_js_path:
        conv = engine.components[Conversation]
        conv.load_conversations(conversations_js_path)


def load_font(engine, font_name, path_to_font):

    interface = engine.components[IFaceManager]

    data = interface.data[interface.id]
    data['fonts'][font_name] = sf.Font.from_file(path_to_font)
