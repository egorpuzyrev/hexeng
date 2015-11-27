#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.engine import Engine

from models.unit import Unit
from models.map import Map
from models.container import Container
from components.movement import Movement
from components.graphics import Graphics
from components.renderer import Renderer

from events.events import *

from support.support import *

import sfml as sf
from random import randint as rnd

import threading
import multiprocessing as mp



def proceed_events():

    while True:
        while engine.events_queue:
            event = engine.poll_event()
            if event:
                if type(event) is DrawEvent:

                    name = event.name
                    x1 = event.x1
                    y1 = event.y1

                    if 'anchor' in event.__dict__:
                        anchor = event.anchor
                    else:
                        anchor = (0, 0)

                    renderer.draw_static(name, x1=x1, y1=y1, anchor=anchor)
                    sf.sleep(sf.milliseconds(10))

                if type(event) is DrawTextureEvent:

                    texture = event.texture

                    window.draw(sf.Sprite(texture))


                elif type(event) is DisplayEvent:
                    window.display()

                elif type(event) is DrawMapEvent:
                    renderer.render_prerendered_map()

                elif type(event) is ClearCanvasEvent:
                    window.clear(sf.Color.BLUE)


                elif type(event) is CloseEvent:
                    exit()

                delta_time = current_time - last_time

                if delta_time > TIMING:


                    sf.sleep(sf.milliseconds(TIMING-delta_time%TIMING+10))


if __name__ == '__main__':

    TIMING = 40

    global engine
    engine = Engine()

    engine.add_container(Map(engine, HORIZ_1, 10, 10))

    engine.add_container(Unit(engine))

    engine.add_component(Movement(engine))

    global sprites
    sprites = Container(engine)

    global spritescontainer
    spritescontainer = Container(engine)

    global graphics
    graphics = Graphics(engine, spritescontainer)


    global window
    window = sf.RenderWindow(sf.VideoMode(640, 480), 'aasdasd')
    window.clear(sf.Color.BLUE)
    window.display()

    global renderer
    renderer = Renderer(engine, graphics, window)

    # ~ unit_id = engine.containers_list[0]

    graphics.load_static('hex40_blue', './resources/hex40_blue.png')

    graphics.load_static('hex40_green_borderless_vertical', './resources/hex40_green_borderless_vertical.png')
    graphics.load_static('hex40_green_borderless_horizontal', './resources/hex40_green_borderless_horizontal.png')
    graphics.load_static('hex40_green_horizontal', './resources/hex40_green_horizontal.png')
    graphics.load_static('hex40_red_horizontal', './resources/hex40_red_horizontal.png')
    graphics.load_static('bullet_anim_1', './resources/bullet1.png')


    graphics.load_animation('bullet_anim_1', '/home/egor/Pictures/bullet1.png')


    global c
    c = sf.Clock()

    global last_time
    last_time = 0

    global current_time
    current_time = 0

    # ~ global mouse
    # ~ mouse = sf.Mouse()

    x0 = 100
    step = 20

    graphics.prerender_map_layer()

    proceed_events_thread = threading.Thread(target=proceed_events, args=())
    # ~ proceed_events_thread = mp.Process(target=proceed_events, args=())
    proceed_events_thread.start()

    engine.push_event(ClearCanvasEvent())

    engine.push_event(DrawMapEvent())

    prev_x = 0
    prev_y = 0

    prev_x1 = 0
    prev_y1 = 0

    t = engine.containers['MAP'].type
    m = engine.containers['MAP']

    temp_texture = sf.RenderTexture(1000, 1000)

    player = Unit(engine)
    enemy = Unit(engine)

    while window.is_open:

        last_time = c.elapsed_time.milliseconds

        engine.push_event(ClearCanvasEvent())

        engine.push_event(DrawMapEvent())

        engine.push_event(EnumerateEvent())

        x ,y = sf.Mouse.get_position(window)

        x1, y1 = nearest(x, y, 40, t)

        cur_x1=t['hex_x'](prev_x1, prev_y1, 40)
        cur_y1=t['hex_y'](prev_x1, prev_y1, 40)

        if not(x1<0 or x1>=m.X or y1<0 or y1>=m.Y):
            if not(x1==prev_x) or not(y1==prev_y):
                # ~ p = pathfind(engine.containers['MAP'], 1, 1, x1, y1, window)
                p = pathfind(engine.containers['MAP'], prev_x1, prev_y1, x1, y1, window)

                p.reverse()

                temp_texture = sf.RenderTexture(1000, 1000)
                temp_texture.clear(sf.Color.TRANSPARENT)

                sprite = graphics.sprites_container.data[graphics.id]['static']['hex40_red_horizontal']

                width = sprite.texture.width
                height = sprite.texture.height

                sprite.origin = (width//2, height//2)

                for i in p:

                    pos_x = t['hex_x'](i[0], i[1], 40)
                    pos_y = t['hex_y'](i[0], i[1], 40)

                    sprite.position = (pos_x, pos_y)

                    temp_texture.draw(sprite)

                temp_texture.display()

                prev_x = x1
                prev_y = y1

            engine.push_event(DrawTextureEvent(texture=temp_texture.texture))

            engine.push_event(DrawEvent(name='bullet_anim_1', x1=cur_x1, y1=cur_y1, anchor=(0.5, 0.5)))

        engine.push_event(DisplayEvent())

        for event in window.events:
            if type(event) is sf.CloseEvent:

                window.close()
                engine.push_event(CloseEvent())
                exit()

            elif type(event) is sf.ResizeEvent:
                window.view = sf.View(sf.Rectangle((0, 0), event.size))

                engine.push_event(ClearCanvasEvent())

                engine.push_event(DrawMapEvent())

                engine.push_event(DisplayEvent())

                print('>>>RESIZEEVENT')

            elif type(event) is sf.MouseWheelEvent:

                step += event.delta

            elif type(event) is sf.MouseButtonEvent:

                if event.pressed:
                    if event.button == sf.Mouse.LEFT:

                        x ,y = event.position
                        # ~ t = engine.containers['MAP'].type
                        x1, y1 = nearest(x, y, 40, t)
                        if x1>0 and x1<m.X and y1>0 and y1<m.Y:
                            m.layers['Walk'][y1][x1] = -1
                            m.layers['Surfaces'][y1][x1] = 'hex40_blue'

                            graphics.update_map_layer(x1, y1, 'hex40_blue')
                            # ~ graphics.prerender_map_layer()

                    elif event.button == sf.Mouse.RIGHT:

                        x ,y = event.position
                        # ~ t = engine.containers['MAP'].type
                        x1, y1 = nearest(x, y, 40, t)


                        # ~ renderer.draw_animation('mans3', t['hex_x'](prev_x1, prev_y1, 40), t['hex_y'](prev_x1, prev_y1, 40), \
                                                # ~ t['hex_x'](x1, y1, 40), t['hex_y'](x1, y1, 40), step=10)
                        p.append(p[-1])
                        for i in range(1, len(p)):

                            x1 = p[i-1][0]
                            y1 = p[i-1][1]

                            x2 = p[i][0]
                            y2 = p[i][1]

                            renderer.draw_animation('bullet_anim_1', int(t['hex_x'](x1, y1, 40)), int(t['hex_y'](x1, y1, 40)), \
                                                int(t['hex_x'](x2, y2, 40)), int(t['hex_y'](x2, y2, 40)), step=10)

                        prev_x1 = x1
                        prev_y1 = y1



        current_time = c.elapsed_time.milliseconds

        delta_time = current_time - last_time

        sf.sleep(sf.milliseconds(TIMING-delta_time%TIMING))
























