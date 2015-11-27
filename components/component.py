#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

# ~from models.unit import Unit

class Component(object):

    # ~def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        # ~if not selfid:
            # ~self.id = str(id(self))
        # ~else:
            # ~self.id = selfid

        self.engine = engineobj

        # ~self.id = self.engine.components_id_manager(self)

        if not engineobj is None:
            if not 'id' in self.__dict__:
                self.id = self.engine.components_id_manager(self)
            self.engine.add_component(self)
        else:
            self.id  = DEFAULTCONTAINERSIDMANAGER(self)


        self.containers_list = []
        self.containers = {}

        # ~self.containers = engineobj.containers
        # ~self.components = engineobj.components

        self.engine.add_component(self)

    def add_container(self, obj):

        self.containers_list.append(obj.id)
        self.containers[obj.id] = obj

    def remove_container(self, objid):

        if objid in self.containers:
            self.containers.pop(self.containers.index(objid))

        if objid in self.containers_d:
            self.containers_d.pop(objid)

    def update(self):

        pass