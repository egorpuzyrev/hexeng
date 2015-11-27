#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

from support.support import *

from random import randint as rnd

import sfml as sf

import threading


texture = sf.Texture.from_file('resources/hex40_blue_fixed_borders.png')

sprite = sf.Sprite(texture)

sprites = [sf.Sprite(texture) for i in range(100)]

print(sprites)

x = sprite.texture_rectangle.width
y = sprite.texture_rectangle.height

sprite.origin = (x//2, y//2)

t = sf.Transform()


rt = sf.RenderTexture(800, 800)
# ~ rt.smooth = 1

w = sf.RenderWindow(sf.VideoMode(640, 480), 'asdasd')

w.clear(sf.Color.GREEN)

# ~ w.display()

c = sf.Clock()

last_time = 0

current_time = 0

while w.is_open:

    for event in w.events:

        if type(event) is sf.CloseEvent:
            w.close()
            exit()
        if type(event) is sf.ResizeEvent:
            w.view = sf.View(sf.Rectangle((0, 0), event.size))


    # ~ sprite.move((rnd(0, 30), rnd(0, 30)+0.1))
# ~
    # ~ sprite.rotate(rnd(-30, +30))
# ~
    # ~ sprite.position = (abs(sprite.position.x % 800), abs(sprite.position.y % 800))

    # ~ rt.clear()

    last_time = c.elapsed_time.seconds

    # ~ rt.draw(sprite)
    # ~ rt.display()

    # ~ res = sf.Sprite(rt.texture)

    w.clear(sf.Color.RED)

    for i in sprites:
        i.move((rnd(0, 30), rnd(0, 30)+0.1))

        i.rotate(rnd(-30, +30))

        i.position = (abs(i.position.x % 800), abs(i.position.y % 800))

        t = threading.Thread(target=w.draw, args=(i,))
        t.start()
        # ~ w.draw(i)

    # ~ w.draw(sf.Sprite(rt.texture))
    # ~ w.draw(sf.Sprite(rt.texture))

    # ~ w.draw(sprite)

    # ~ sf.sleep(sf.milliseconds(20))

    w.display()

    current_time = c.elapsed_time.seconds

    print('FPS: ', 1/(current_time-last_time))