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
            # ~self.id  = DEFAULTCOMPONENTSIDMANAGER(self)


        self.containers_list = []
        self.containers = {}

        self.handlers = {}

        # ~self.containers = engineobj.containers
        # ~self.components = engineobj.components

        self.engine.add_component(self)

        print(">>INITIALIZED COMPONENT {} ID {}".format(type(self), self.id))

    def add_container(self, obj):

        self.containers_list.append(obj.id)
        self.containers[obj.id] = obj

    def remove_container(self, objid):

        if objid in self.containers:
            self.containers.pop(self.containers.index(objid))

        if objid in self.containers_d:
            self.containers_d.pop(objid)

    def bind(self, event_type, handler, mode='+'):

        if self.handlers.get(event_type) is None:
            self.handlers[event_type] = []
            
        if mode=='+':
            self.handlers[event_type].append(handler)
        elif mode=='-':
            self.handlers[event_type] = [handler, ]
        # ~print(">>>BINDED:", self.id, type(self), event_type, self.handlers[event_type])
            
    def update(self, event):
        
        event_type = type(event)
        
        if event_type in self.handlers:
            # ~print(self.id, event_type)
            for handler in self.handlers[event_type]:
                handler(self, event)
