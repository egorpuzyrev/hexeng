#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

import sfml as sf

from engine.engine import Engine

from models.unit import Unit
from models.container import Container
from components.movement import Movement
from components.component import Component


class GraphicsSystem(Component, Container):

    # ~ def __init__(self, engineobj=None, selfid=None):
    def __init__(self, engineobj=None):

        # ~ if not selfid:
            # ~ self.id = str(id(self))
        # ~ else:
            # ~ self.id = selfid

        self.engine = engineobj

        # ~ self.window = sf.RenderWindow(sf.VideoMode(640, 480), 'Test')



