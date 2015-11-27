#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')


class Action(Component):

    # ~ def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        super().__init__(engineobj)

        self.actions = {}

        self.mapobj = engineobj.mapobj
        self.units = engineobj.units

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = []

    def bind_action(self, objid, action, order=-1):

        data = self.units[objid].data[self.id]

        # ~ if not objid in self.actions:
            # ~ self.units[objid].data[self.id] = []

        if order==-1:
            data.apend(action)
        else:
            data.insert(order, action)

    def do(self, objid):

        for i in data:
            i(self)

