#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

# ~from engine.engine import Engine

# ~from models.unit import Unit
# ~from models.container import Container

# ~from .unit import Unit
from .container import Container

# ~from components.movement import Movement
# ~from components.component import Component

from support.support import *

class Map(Container):

    # ~def __init__(self, engineobj=None, selfid=None, maptype='', sizex=0, sizey=0, *layers, **components):
    def __init__(self, engineobj=None, maptype=VERT_0, sizex=0, sizey=0, *layers, **components):

        self.id = 'MAP'

        super().__init__(engineobj, *components)

        self.type = maptype

        self.X = sizex
        self.Y = sizey

        self.components = {}

        self.layers = {}
        self.layers_order = []

        self.add_layer('Textures')

        if layers:
            for i in layers:
                self.add_layer(i)
        else:
            for i in ['Surfaces', 'Units', 'Buildings', 'Walk']:
                self.add_layer(i)

            # ~self.layers['Surfaces'] = [[0 for i in range(self.X)] for j in range(self.Y)]


    def add_layer(self, name, content=None):

        if not name in self.layers:
            self.layers_order.append(name)
            if content is None:
                self.layers[name] = [[0 for i in range(self.X)] for j in range(self.Y)]
            else:
                self.layers[name] = content

    def set_layer(self, name, content):
        self.layers[name] = content

    def expand(self, dx=1, dy=1):

        layers = self.layers

        for i in layers: # dict
            for j in range(len(layers[i])): # list of lists
                layers[i][j] += [0 for k in range(dx)]

            layers[i] += [[0 for k in range(self.X+dx)] for l in range(dy)]

        self.X += dx
        self.Y += dy

    def swap(self, x1, y1, x2, y2, layer='Units'):

        layers = self.layers

        layers[layer][y1][x1], layers[layer][y2][x2] = layers[layer][y2][x2], layers[layer][y1][x1]


    def get_cell(self, x1, y1):

        layers = self.layers

        return layers[y1][x1]
