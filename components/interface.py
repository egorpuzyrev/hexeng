#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import json

import sfml as sf


def IFaceManager(object):

    def __init__(self, engineobj=None, graphicscomponent=None, window=None):
        super().__init__(engineobj)

        self.graphics_component = graphicscomponent
        self.add_container(graphicscomponent)
        self.graphics_component_id = graphicscomponent.id

        self.window = window

        self.widgets_order = []
        self.wingets = {}

    def add_widget(self, widget):

        

        # ~self.widgets_order 
