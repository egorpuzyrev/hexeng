#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#~ import pdb

import numbers

from engine.engine import Engine
from models.unit import Unit
from models.map import Map
from models.container import Container
from components.movement import Movement
from components.attributes import Attributes
from components.graphics import Graphics
from components.renderer import Renderer

from events.events import *

from support.support import *

import sfml as sf
#~ from sfml import sf
from random import randint as rnd

#~ import threading
#~ import multiprocessing as mp



def proceed_events():


    while engine.events_queue:
        event = engine.poll_event()
        if event:
            if type(event) is DrawStaticEvent:

                name = event.name
                x1 = event.x1
                y1 = event.y1

                if 'anchor' in event.__dict__:
                    anchor = event.anchor
                else:
                    anchor = (0, 0)

                if 'rectangle' in event.__dict__:
                    rectangle = event.rectangle
                else:
                    rectangle = sf.Rectangle((0, 0), (S, S)) # None

                # ~print('RRECTANGLE:', rectangle)

                renderer.draw_static(name, x1=x1, y1=y1, anchor=anchor, rectangle=rectangle)

                sf.sleep(sf.milliseconds(10))

            if type(event) is DrawTextureEvent:

                texture = event.texture

                window.draw(sf.Sprite(texture))


            elif type(event) is DisplayEvent:
                window.display()

            elif type(event) is DrawMapEvent:

                layer = event.layer

                renderer.render_prerendered_map(layer)

            elif type(event) is ClearCanvasEvent:
                window.clear(sf.Color.BLUE)


            elif type(event) is UpdateMapLayerEvent:

                x1 = event.x1
                y1 = event.y1
                texture = event.texture
                layer = event.layer

                graphics.update_map_layer(x1=x1, y1=y1, texture=texture, layer=layer)


            elif type(event) is ShowHealthEvent:

                objid = event.objid

                data = engine.containers[objid].data

                health = data[attributes.id]['attributes']['health']

                ux = data[movement.id]['x']
                uy = data[movement.id]['y']

                x1 = t['hex_x'](ux, uy, S)
                y1 = t['hex_y'](ux, uy, S)

                healthbar = sf.RectangleShape()
                healthbar.outline_color = sf.Color.BLACK
                healthbar.fill_color = sf.Color.RED
                healthbar.outline_thickness = 2
                healthbar.size=(health*0.4*S/100, S//10)
                healthbar.origin = (health*0.4*S/100//2, S//20)
                healthbar.position = (x1, y1-S//2-15)


                window.draw(healthbar)
                # ~window.display()



            elif type(event) is CloseEvent:
                exit()


            elif type(event) is UpdateSceneEvent:

                pass








if __name__ == '__main__':



    TIMING = 30

    global engine
    engine = Engine()

    engine.add_container(Map(engine, HORIZ_1, 15, 15))





    global sprites
    sprites = Container(engine)

    global spritescontainer
    spritescontainer = Container(engine)

    global graphics
    graphics = Graphics(engine, spritescontainer)

    global window
    window = sf.RenderWindow(sf.VideoMode(800, 600), 'aasdasd')
    window.clear(sf.Color.BLUE)
    window.display()

    global renderer
    renderer = Renderer(engine, graphics, window)

    global c
    c = sf.Clock()

    global last_time
    last_time = 0

    global current_time
    current_time = 0




    global player
    player = Unit(engine)

    global enemy
    enemy = Unit(engine)

    global movement
    movement = Movement(engine)

    global attributes
    attributes = Attributes(engine)

    player.add_component(movement)
    enemy.add_component(movement)

    player.add_component(graphics)
    enemy.add_component(graphics)

    player.add_component(attributes)
    enemy.add_component(attributes)

    attributes.add_attribute(player.id, 'health', 100)
    attributes.add_attribute(enemy.id, 'health', 100)

    #~ print('ENGINE COMPONENTS:', engine.components)

    graphics.load_static('hex40_blue', './resources/hex40_blue.png')

    graphics.load_static('hex40_green_borderless_vertical', './resources/hex40_green_borderless_vertical.png')
    graphics.load_static('hex40_green_borderless_horizontal', './resources/hex40_green_borderless_horizontal.png')
    graphics.load_static('hex40_green_horizontal', './resources/hex40_green_horizontal.png')
    graphics.load_static('hex40_red_horizontal', './resources/hex40_red_horizontal.png')
    graphics.load_static('bullet_anim_1', './resources/bullet1.png')

    # ~graphics.load_static('stone2', './resources/stone2_horizontal.png')
    graphics.load_static('stone2', './resources/stone2_80_horizontal.png')

    # ~graphics.load_static('sheriff', './resources/sheriff.png')
    # ~graphics.load_animation('sheriff', './resources/sheriff.png')
    graphics.load_static('sheriff', './resources/sheriff_80.png')
    graphics.load_animation('sheriff', './resources/sheriff_80.png')

    graphics.load_static('policeman', './resources/policeman.png')
    graphics.load_animation('policeman', './resources/policeman.png')

    graphics.load_static('policeman_walking', './resources/policeman_walking4.png')
    graphics.load_animation('policeman_walking', './resources/policeman_walking4.png')

    graphics.load_animation('bullet_anim_1', './resources/bullet1.png')


    graphics.bind_sprite(player.id, 'sheriff')
    graphics.bind_animation(player.id, 'sheriff')

    graphics.bind_sprite(enemy.id, 'policeman')
    graphics.bind_animation(enemy.id, 'policeman')


    t = engine.containers['MAP'].type
    m = engine.containers['MAP']

    m.layers['Units'][0][0] = player.id
    m.layers['Units'][9][9] = enemy.id

    m.layers['Walk'][0][0] = -2
    m.layers['Walk'][9][9] = -2

    enemy.data[movement.id]['x'] = 9
    enemy.data[movement.id]['y'] = 9

    m.add_layer('UnitsTextures')

    x0 = 100
    step = 20

    m.layers['Surfaces'] = [['stone2' for i in range(m.X)] for j in range(m.Y)]

    graphics.prerender_map_layer('Surfaces')
    graphics.prerender_map_layer('UnitsTextures')

    engine.push_event(ClearCanvasEvent())

    engine.push_event(DrawMapEvent(layer='Surfaces'))
    engine.push_event(DrawMapEvent(layer='UnitsTextures'))

    prev_x = 0
    prev_y = 0

    prev_x1 = 0
    prev_y1 = 0



    temp_texture = sf.RenderTexture(t['hex_x'](m.X+1, m.Y+1, S), t['hex_y'](m.X+1, m.Y+1, S))


    while window.is_open:

        last_time = c.elapsed_time.milliseconds

        engine.push_event(ClearCanvasEvent())

        graphics.prerender_map_layer('UnitsTextures')

        engine.push_event(DrawMapEvent(layer='Surfaces'))

        engine.push_event(DrawMapEvent(layer='UnitsTextures'))
        engine.push_event(ShowHealthEvent(objid=player.id))
        engine.push_event(ShowHealthEvent(objid=enemy.id))


        # ~x ,y = sf.Mouse.get_position(window)
        x ,y = sf.Mouse.get_position(window)

        size_x, size_y = window.size
        cx, cy = window.view.center
        dcx = 0
        dcy = 0

        if size_y>y>size_y-20:
            dcy = 10
            # ~window.view.center = (cx, cy+10)
        elif 0<y<20:
            dcy = -10
            # ~window.view.center = (cx, cy-10)

        if size_x>x>size_x-20:
            dcx = 10
            # ~window.view.center = (cx+10, cy)
        elif 0<x<20:
            dcx = -10
            # ~window.view.center = (cx-10, cy)
        if dcx or dcy:
            window.view.center = (cx+dcx, cy+dcy)

        # ~print('window.view.center:', window.view.center)


        x ,y = window.map_pixel_to_coords(sf.Mouse.get_position(window))

        x1, y1 = nearest(x, y, S, t)

        cur_x1=t['hex_x'](prev_x1, prev_y1, S)
        cur_y1=t['hex_y'](prev_x1, prev_y1, S)

        if not(x1<0 or x1>=m.X or y1<0 or y1>=m.Y):
            if not(x1==prev_x) or not(y1==prev_y):

                # ~p = pathfind(m, prev_x1, prev_y1, x1, y1)

                px = player.data[movement.id]['x']
                py = player.data[movement.id]['y']

                pp = find_on_deep(m, px, py, 3)
                ps = []
                for i in pp:
                    ps.extend(i)

                ps.reverse()

                temp_texture = sf.RenderTexture(t['hex_x'](m.X+1, m.Y+1, S), t['hex_y'](m.X+1, m.Y+1, S))
                temp_texture.clear(sf.Color.TRANSPARENT)

                sprite = graphics.sprites_container.data[graphics.id]['static']['hex40_red_horizontal']

                width = sprite.texture.width
                height = sprite.texture.height

                sprite.origin = (width//2, height//2)

                for i in ps:

                    pos_x = t['hex_x'](i[0], i[1], S)
                    pos_y = t['hex_y'](i[0], i[1], S)

                    sprite.position = (pos_x, pos_y)

                    temp_texture.draw(sprite)

                temp_texture.display()

                prev_x = x1
                prev_y = y1

            engine.push_event(DrawTextureEvent(texture=temp_texture.texture))



        px = player.data[movement.id]['x']
        py = player.data[movement.id]['y']
        engine.push_event(DrawStaticEvent(name='sheriff', x1=t['hex_x'](px, py, S), \
                                                    y1=t['hex_y'](px, py, S), \
                                                    anchor=(0.5, 0.5)))
        ex = enemy.data[movement.id]['x']
        ey = enemy.data[movement.id]['y']
        engine.push_event(DrawStaticEvent(name='policeman', x1=t['hex_x'](ex, ey, S), \
                                                      y1=t['hex_y'](ex, ey, S), \
                                                      anchor=(0.5, 0.5)))

        engine.push_event(ShowHealthEvent(objid=player.id))
        engine.push_event(ShowHealthEvent(objid=enemy.id))

        engine.push_event(DisplayEvent())

        for event in window.events:
            if type(event) is sf.CloseEvent:

                window.close()
                engine.push_event(CloseEvent())
                exit()

            elif type(event) is sf.ResizeEvent:
                #~ window.view = sf.View(sf.Rectangle((0, 0), event.size))
                window.view = sf.View((0, 0, event.size[0], event.size[1]))

                engine.push_event(ClearCanvasEvent())

                engine.push_event(DrawMapEvent(layer='Surfaces'))
                engine.push_event(DrawMapEvent(layer='UnitsTextures'))

                engine.push_event(DisplayEvent())

            elif type(event) is sf.MouseWheelEvent:

                print('ZOOM:', zoom_coeff(4, event.delta))
                window.view.zoom(zoom_coeff(1.25, -event.delta))


            elif type(event) is sf.MouseButtonEvent:
                print('event.position', event.position)
                print('sf.Mouse.get_position()', sf.Mouse.get_position())
                print('sf.Mouse.get_position(window)', sf.Mouse.get_position(window))
                print('map_pixel_to_coords:', window.map_pixel_to_coords(event.position))

                if event.pressed:
                    if event.button == sf.Mouse.LEFT:

                        pass

                    elif event.button == sf.Mouse.RIGHT:

                        pass







        proceed_events()

        current_time = c.elapsed_time.milliseconds

        delta_time = current_time - last_time

        sf.sleep(sf.milliseconds(TIMING-delta_time%TIMING))
