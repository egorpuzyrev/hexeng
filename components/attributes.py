#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from components.component import Component
from models.unit import Unit
from models.container import Container

class Attributes(Component):

    # ~ name = 'Movement'

    # ~ def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        super().__init__(engineobj)

        # ~self.containers = engineobj.containers
        # ~self.components = engineobj.components
        # ~self.containers = []
        # ~self.components = []
        self.mapobj = engineobj.containers['MAP']

        self.keepers = {}

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {'attributes_list': [],
                             'attributes': {}
                             }

    def add_attribute(self, objid, name, value=None):

        data = self.containers[objid].data[self.id]

        data['attributes_list'].append(name)
        data['attributes'][name] = value

        if not name in self.keepers:
            self.keepers[name] = []

        self.keepers[name].append(objid)

    def set_attribute(self, objid, name, value):

        data = self.containers[objid].data[self.id]

        data['attributes'][name] = value

    def get_attribute(self, objid, name):

        data = self.containers[objid].data[self.id]
        if name in data['attributes']:
            return data['attributes'][name]
        else:
            return None

