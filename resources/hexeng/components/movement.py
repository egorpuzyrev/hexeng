#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from components.component import Component
from models.unit import Unit
from models.container import Container

class Movement(Component):

    # ~ name = 'Movement'

    # ~ def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        super().__init__(engineobj)

        self.containers = engineobj.containers
        self.components = engineobj.components

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {}
        obj.data[self.id]['x'] = 0
        obj.data[self.id]['y'] = 0

    def get_coords(self, objid):

        x = self.units[objid].data[self.id]['x']
        y = self.units[objid].data[self.id]['y']

        return (x, y)

    def move(self, objid, dx=0, dy=0, layer='Units'):

        x = self.units[objid].data[self.id]['x']
        y = self.units[objid].data[self.id]['y']


        if layer in self.mapobj.layers:
            if not self.mapobj.layers[self.layer][y0+dy][x0+dx]==0:
                self.mapobj.layers[self.layer][y0+dy][x0+dx] = self.mapobj.layers[self.layer][y0][x0]
                self.mapobj.layers[self.layer][y0][x0] = 0

                x0 += dx
                y0 += dy