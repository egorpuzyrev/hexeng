#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from .component import Component
# ~from models.unit import Unit
# ~from models.container import Container
# ~from components.components import *
# ~from models.models import *

class Movement(Component):

    # ~name = 'Movement'

    # ~def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        super().__init__(engineobj)

        # ~self.containers_list = []
        # ~self.containers = {}
        if 'MAP' in engineobj.containers:
            self.mapobj = engineobj.containers['MAP']

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {}
        obj.data[self.id]['x'] = 0
        obj.data[self.id]['y'] = 0
        obj.data[self.id]['prev_x'] = 0
        obj.data[self.id]['prev_y'] = 0

    def get_coords(self, objid):

        x = self.containers[objid].data[self.id]['x']
        y = self.containers[objid].data[self.id]['y']

        return (x, y)

    def set_coords(self, objid, x, y):

        self.containers[objid].data[self.id]['x'] = x
        self.containers[objid].data[self.id]['y'] = y


    def get_prev_coords(self, objid):

        prev_x = self.containers[objid].data[self.id]['prev_x']
        prev_y = self.containers[objid].data[self.id]['prev_y']

        return (x, y)

    def move_on_layer(self, objid, dx=0, dy=0, layer='UnitsTextures'):

        obj = self.containers[objid]

        x0 = obj.data[self.id]['x']
        y0 = obj.data[self.id]['y']


        # ~print('LAYER:', layer)
        # ~print('Y:', len(self.mapobj.layers[layer]))
        # ~print('X:', len(self.mapobj.layers[layer][0]))
        # ~print('Y0:', y0)
        # ~print('X0:', x0)
        # ~print('DY:', dy)
        # ~print('DX:', dx)

        if layer in self.mapobj.layers:
            # ~if self.mapobj.layers[layer][y0+dy][x0+dx]==0:
            self.mapobj.layers[layer][y0+dy][x0+dx], self.mapobj.layers[layer][y0][x0] = self.mapobj.layers[layer][y0][x0], self.mapobj.layers[layer][y0+dy][x0+dx]
                # ~self.mapobj.layers[layer][y0][x0] = 0

                # ~obj.data[self.id]['prev_x'] = x0
                # ~obj.data[self.id]['prev_y'] = y0
# ~
                # ~obj.data[self.id]['x'] += dx
                # ~obj.data[self.id]['y'] += dy

                #~ print('MOVED', self.mapobj.layers[layer][y0+dy][x0+dx])

        #~ print('NOW AT:', obj.data[self.id]['x'], obj.data[self.id]['y'])

                # ~x0 += dx
                # ~y0 += dy

    def move(self, objid, dx=0, dy=0):
        obj = self.containers[objid]

        x0 = obj.data[self.id]['x']
        y0 = obj.data[self.id]['y']

        obj.data[self.id]['prev_x'] = x0
        obj.data[self.id]['prev_y'] = y0

        obj.data[self.id]['x'] += dx
        obj.data[self.id]['y'] += dy

        # ~for layer in self.mapobj.layers_order:
        for layer in self.mapobj.layers:
            # ~print("LAYER:", layer)
            # ~self.move_on_layer(objid, dx, dy, layer=layer)
            print(">>>MOVE ON <AP LAYER:", layer)
            self.mapobj.layers[layer][y0+dy][x0+dx], self.mapobj.layers[layer][y0][x0] = self.mapobj.layers[layer][y0][x0], self.mapobj.layers[layer][y0+dy][x0+dx]


    
    def moveto(self, objid, x2=0, y2=0):
        obj = self.containers[objid]

        x0 = obj.data[self.id]['x']
        y0 = obj.data[self.id]['y']

        dx = x2 - x0
        dy = y2 - y0

        # ~for layer in self.mapobj.layers_order:
            # ~print("LAYER:", layer)
            # ~self.move_on_layer(objid, dx, dy, layer=layer)
        self.move(objid, dx, dy)

        obj.data[self.id]['prev_x'] = x0
        obj.data[self.id]['prev_y'] = y0

        obj.data[self.id]['x'] = x2
        obj.data[self.id]['y'] = y2
