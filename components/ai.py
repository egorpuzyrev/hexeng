#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import sys
sys.path.append('../')

# ~from components.components import *
from .component import *

from .movement import *

from .attributes import *

from models.models import *
# ~from engine.engine import Engine

# ~from support.support import *

import sfml as sf
#~ from sfml import sf


class AI(Component):

    def __init__(self, engineobj=None):

        super().__init__(engineobj)


    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {
                            }

    def update(self):
        
        e = self.engine
        m = self.engine.containers['MAP']
        mov = self.engine.components[Movement]
        a = self.engine.components[Attributes]
        
        
        
        players_ids = filter(lambda x: Movement in e.containers[x].data and not type(self) in e.containers[x].data, e.containers)
        players_coords = [mov.get_coords(i) for i in players_ids]
        print('players_coords:', players_coords)
        ai_ids = filter(lambda x: Movement in e.containers[x].data and type(self) in e.containers[x].data, e.containers)
        ai_coords = [mov.get_coords(i) for i in ai_ids]
        print('ai_coords:', ai_coords)
        
        targets = {}
        
        for j in ai_coords:
            targets[j] = ((1000, 1000), 10000)
            tt = targets[j]
            ax, ay = j
            for i in players_coords:
                px, py = i
                r = sqrt((ax-px)**2 + (ay-py)**2)
                if r < tt[1]:
                    tt = ((px, py), r)
            
            targets[j] = tt[0]
        
        ways = {}
        
        for i in targets:
            ways[i] = pathfind(m, targets[i][0], targets[i][1], i[0], i[1])
        
        for i in ways:
            if ways[i]:
                uid = m.layers['Units'][i[1]][i[0]]
                ap = a.get_attribute(uid, 'action_points')
                path = (ways[i][:-1])[:ap]
                print(i, path)
                mov.moveto(uid, path[-1][0], path[-1][1])
            
                
                
        
