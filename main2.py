#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys



import numbers

from components.components import *
from models.models import *


from engine.engine import *

from events.events import *

from support.support import *

from support.load_support import *

import json

import sfml as sf


def setup_app():
     # allows to build .exe

    if '_MEIPASS2' in os.environ:
        sys._MEIPASS = os.environ['_MEIPASS2']
        # Ensure sys._MEIPASS is absolute path.
        sys._MEIPASS = os.path.normpath(sys._MEIPASS)
        sys._MEIPASS = os.path.abspath(sys._MEIPASS)
        # Delete _MEIPASS2 from environment.
        del os.environ['_MEIPASS2']

    sys._MEIPASS = sys._MEIPASS2 = resource_path(".")
    
    global _MEIPASS
    global _MEIPASS2
    _MEIPASS = _MEIPASS2 = resource_path(".")



if __name__=='__main__':

    setup_app() # allows to build .exe

    print('Seems, it works')
