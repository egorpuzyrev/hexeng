#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

import time

import numbers

from components.components import *
from models.models import *

from engine.engine import *

N = 1000

if __name__=='__main__':

    

    e = Engine()

    e.add_container(Map(e, maptype=HORIZ_0, sizex=20, sizey=20))
    m = e.containers['MAP']
    t = m.type

    movement = Movement(e)

    units = [Unit(e, movement) for i in range(N)]


    while True:
        start = time.clock()

        for u in units:
            # ~movement.get_coords(u.id)
            movement.move(u.id, 0, 0)

        finish = time.clock()

        print(finish - start, N/(finish-start), 'per sec')

    
