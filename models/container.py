    #!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from support.support import *


class Container(object):

    # ~def __init__(self, engineobj=None, selfid=None, *components):
    def __init__(self, engineobj=None, *components):

        # ~if not selfid:
            # ~self.id = str(id(self))
        # ~else:
            # ~self.id = selfid

        self.engine = engineobj

        if not engineobj is None:
            if not 'id' in self.__dict__:
                self.id = self.engine.containers_id_manager(self)
            self.engine.add_container(self)
        else:
            self.id  = DEFAULTCONTAINERSIDMANAGER(self)

        self.data = {}

        self.components = {}
        self.components_order = []


        for i in components:
            self.add_component(i)



    def add_component(self, component, order=-1, name=''):

        if not name:
            name = component.id

        self.components[name] = component

        if order==-1:
            self.components_order.append(component)
        else:
            self.components_order.insert(order, component)

        component.add_container(self)

    def remove_component(self, name):

        if name in self.components:
            self.components[name].remove_container(self.id)
            self.components.pop(name)

        if name in self.components_order:
            self.components_order.pop(self.components_order.index(name))

    def update_component(self, name):

        if name in self.components:
            self.components[name].update()

    def update_all(self):

        for i in self.components_order:
            self.components[i].update()

    def get_components_list(self):

        return list(self.components.keys())