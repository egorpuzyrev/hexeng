#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from .container import Container

class Unit(Container):

    def __init__(self, engineobj=None, *components):

        super().__init__(engineobj, *components)


if __name__=='__main__':

    u = Unit()

    #~ print(u.components)

