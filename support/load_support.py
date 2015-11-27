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


def load_map_from_file(m, g, path):

    path = resource_path(path)

    with open(path) as f:
        s = f.read()
        f.close()

    j = json.loads(s)

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


def load_level(e, tex_path, map_path, conv_path):
    
    m = e.containers['MAP']
    
    g = e.components[Graphics]
    
    conv = e.components[Conversation]
    
    load_textures_from_file(g, tex_path)
    load_map_from_file(m, g, map_path)
    conv.load_conversations(conv_path)

    create_units_by_map(e)
    
    e.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'Buildings', 'UnitsTextures']))
