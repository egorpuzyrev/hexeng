#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Engine class contain links to all containers and components in game and serves game loop.
Every new container/component requires Engine class as parameter whili initializing.
"""


import sys
sys.path.append('../')


from support.support import *


class Event(object):

    def __init__(self, eventtype, **kwargs):
        self.__dict__.update(event_type=eventtype, **kwargs)


class Engine(object):

    def __init__(self, containersidmanager=DEFAULTCONTAINERSIDMANAGER, componentsidmanager=DEFAULTCOMPONENTSIDMANAGER):
        """
        Engine requires 'id managers' to automatically set object id.
        containersidmanager - id manager for containers. In default, it's just returns id of container object.
        componentsidmanager - id manager for components. In default, it's just returns type of component object.
        """

        self.idmanager = containersidmanager
        self.containers_id_manager = containersidmanager
        self.components_id_manager = componentsidmanager

        # ~if not selfid:
            # ~self.id = str(id(self))
        # ~else:
            # ~self.id = selfid

        self.id = self.idmanager(self)

        self.events_queue = []

        self.update_queue = []

        self.systems_list = []
        self.systems = {}

        self.components_list = []
        self.components = {}

        self.containers_list = []
        self.containers = {}

    def push_event(self, event):

        self.events_queue.append(event)

    def poll_event(self):
        """
        Polls event form events queue.
        """

        if self.events_queue:
            return self.events_queue.pop(0)
        else:
            return None

    def add_component(self, obj):
        if not obj.id in self.components:
            self.components[obj.id] = obj
            self.components_list.append(obj.id)
            self.update_queue.append(obj.id)

    def add_container(self, obj):
        if not obj.id in self.containers:
            self.containers[obj.id] = obj
            self.containers_list.append(obj.id)


    def add_system(self, obj):
        if not obj.id in self.systems:
            self.systems[obj.id] = obj
            self.systems_list.append(obj.id)
            self.update_queue.append(obj.id)

    def update_all(self):
        for i in self.update_queue:
            # ~i.update()
            pass

    def update_system(self, objid):

        self.systems[objid].update()

    def update_component(self, objid):

        self.components[objid].update()