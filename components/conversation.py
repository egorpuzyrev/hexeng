#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import sys
sys.path.append('../')

# ~from components.components import *
from .component import *

from models.models import *
# ~from engine.engine import Engine

from support.support import *
from events.events import *

import sfml as sf
#~ from sfml import sf

import json


class Conversation(Component):

    def __init__(self, engineobj=None, convcontainer=None):

        super().__init__(engineobj)

        self.conversations_container = convcontainer
        self.add_container(convcontainer)
        self.conversations_container_id = convcontainer.id


        self.counter = 0

    def add_container(self, obj):

        super().add_container(obj)

        obj.data[self.id] = {'conversations': {}
                            }


    def load_conversations(self, path, **kwargs):
        """Loads static sprites from file usable for SFML"""

        objid = self.conversations_container.id

        if not objid in self.containers:
            raise Exception("Object %s has no such (%s) component" %(objid, type(self)))
        else:
            data = self.containers[objid].data[self.id]

            try:
                
                with open(path) as f:
                    s = f.read()
                    j = json.loads(s)
                    # ~conv_order = j['conversations_order']
                    data['conversations'].update(j)
            except:
                raise Exception("File %s not found or corrupted" %(path, ))

    def start_conversation(self, name):
        conv = self.conversations_container.data[self.id]['conversations'][name]
        self.engine.push_event(AskEvent(conversation=conv))

    def get_last_answer(self, name):
        conv = self.conversations_container.data[self.id]['conversations'][name]
        return conv['.lastanswer']
