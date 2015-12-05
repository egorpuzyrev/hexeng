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
    _MEIPASS = _MEIPASS2 = resource_path(".")



def Graphics_UpdateScene_Handler(obj, event):
    # ~if type(event) is UpdateSceneEvent:
    layers_order = event.layers_order
    sprites = obj.sprites_container.data[obj.id]
    # ~for l in layers_order:
        # ~renderer.draw_map_layer(layer=l)
    # ~print(">>>>EVENT:", event)

def Renderer_UpdateScene_Handler(obj, event):
    # ~print("Renderer_UpdateScene_Handler")
    # ~if type(event) is UpdateSceneEvent:
    layers_order = event.layers_order
    # ~sprites = graphics.sprites_container.data[graphics.id]
    for l in layers_order:
        obj.draw_map_layer(layer=l)


if __name__=='__main__':

    setup_app() # allows to build .exe

    print('Seems, it works')

    engine = Engine()
    engine.add_container(Map(engine, maptype=HORIZ_0, sizex=20, sizey=20))


    m = engine.containers['MAP']
    t = m.type

    # ~m.add_layer('UnitsTextures', content=[[0 for j in range(m.X)] for i in range(m.Y)])

    # ~load_map_from_file(m, graphics, 'test_map.js')

    graphics = Graphics(engine, Container(engine))
    graphics.bind(UpdateSceneEvent, Graphics_UpdateScene_Handler)

    window = sf.RenderWindow(sf.VideoMode(800, 600), 'HEX')

    renderer = Renderer(engine, graphics, window)
    renderer.bind(UpdateSceneEvent, Renderer_UpdateScene_Handler)

    iface = IFaceManager(engine, Container(), window)

    mwid = MasterWidget(iface)
    btn1 = Button(mwid)

    attributes = Attributes(engine)

    movement = Movement(engine)
    
    ai = AI(engine)
    
    conversation = Conversation(engine, Container(engine))
    
    # ~conversation.load_conversations('conversations.js')
    # ~load_textures_from_file(graphics, 'textures.js')
    # ~load_map_from_file(m, graphics, 'map.js')
    # ~create_units_by_map(engine)

    load_level(engine, 'textures.js', 'map.js', 'conversations.js')

    # ~engine.add_container(Unit(engine, graphics, attributes, movement))


    clock = sf.Clock()
    last_time = 0
    current_time = clock.elapsed_time.milliseconds


    cur_uid = 0
    unit = 0

    total_zoom = 1

    circle = sf.CircleShape(R(S), 6)
    # ~circle.radius = R(S)
    circle.outline_color = sf.Color(130, 220, 200, 200)
    circle.fill_color = sf.Color.TRANSPARENT
    circle.outline_thickness = 7
    circle.origin = (R(S), R(S))

    circle1 = sf.CircleShape(R(S)//2, 6)
    # ~circle1.radius = R(S)//2
    # ~circle1.outline_color = sf.Color(230, 120, 100, 255)
    circle1.outline_color = sf.Color(130, 220, 200, 200)
    circle1.fill_color = sf.Color.TRANSPARENT
    circle1.outline_thickness = 10
    circle1.origin = (R(S)//2, R(S)//2)

    circle2 = sf.CircleShape(R(S)//2, 6)
    # ~circle2.radius = R(S)//2
    # ~circle2.outline_color = sf.Color(230, 120, 100, 255)
    circle2.outline_color = sf.Color(230, 120, 100, 200)
    circle2.fill_color = sf.Color.TRANSPARENT
    circle2.outline_thickness = 10
    circle2.origin = (R(S)//2, R(S)//2)



    graphics.prerender_map_layer(layer='Surfaces')
    graphics.prerender_map_layer(layer='UnitsTextures')
    graphics.prerender_map_layer(layer='Buildings')

    while window.is_open:

        last_time = clock.elapsed_time.milliseconds

        x, y = window.map_pixel_to_coords(sf.Mouse.get_position(window))

        # ~graphics.prerender_map_layer(layer='UnitsTextures')
        engine.push_event(ClearCanvasEvent())
        engine.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'Buildings', 'UnitsTextures']))
        if cur_uid>0:
            engine.push_event(OutlineUnitEvent(uid=cur_uid))
            engine.push_event(ShowPossibleWaysEvent(uid=cur_uid))
            nx, ny = nearest(x, y, S, t)
            engine.push_event(ShowWayEvent(x1=nx, y1=ny))
        else:
            graph = []
            possible_cells = []


        # ~if cur_conv:
            # ~engine.push_event(AskEvent(conversation=cur_conv))

        engine.push_event(DisplayEvent())

        x, y = sf.Mouse.get_position(window)

        window_size_x, window_size_y = window.size
        cx, cy = window.view.center
        dcx = 0
        dcy = 0

        if window_size_y>y>window_size_y-SCROLLZONE:
            dcy = 10
        elif 0<y<SCROLLZONE:
            dcy = -10
        if window_size_x>x>window_size_x-SCROLLZONE:
            dcx = 10
        elif 0<x<SCROLLZONE:
            dcx = -10
        if dcx or dcy:
            window.view.center = (cx+dcx, cy+dcy)


        for event in window.events:

            # ~print(">>>EVENT:", type(event))

            if type(event) is sf.CloseEvent:
                window.close()
                exit()

            elif type(event) is sf.ResizeEvent:
                window.view = sf.View((0, 0, event.size[0], event.size[1]))
                window.view.zoom(total_zoom)
                engine.push_event(ClearCanvasEvent())
                engine.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'UnitsTextures']))
                engine.push_event(DisplayEvent())

            elif type(event) is sf.MouseWheelEvent:

                # ~print('ZOOM:', zoom_coeff(4, event.delta))
                print('TOTAL_ZOOM:', total_zoom)
                zoom = zoom_coeff(1.25, -event.delta)
                total_zoom *= zoom
                window.view.zoom(zoom)

            elif type(event) is sf.MouseButtonEvent:
                button = event.button

                x, y = window.map_pixel_to_coords(event.position)
                map_x, map_y = nearest(x, y, S, t)
                hex_x = t['hex_x'](map_x, map_y, S)
                hex_y = t['hex_y'](map_x, map_y, S)

                if button == sf.Mouse.LEFT and event.pressed:
                    cur_uid = m.layers['Units'][map_y][map_x]

                    if cur_uid > 0 and not AI in engine.containers[cur_uid].data:
                        # ~x, y = window.map_pixel_to_coords(event.position)
                        # ~map_x, map_y = nearest(x, y, S, t)
                        
                        print("CUR_ID:", cur_uid)
                        if cur_uid:
                            conversation.start_conversation('dialog1')
                            # ~ans = ask(window, message=conversation['.start']['message'], answers=conversation['.start']['answers'])
                            # ~while ans in conversation:
                                # ~ans = ask(window, message=conversation[ans]['message'], answers=conversation[ans]['answers'])
                    else:
                        cur_uid = 0
                if button == sf.Mouse.RIGHT and event.pressed:

                    if cur_uid:

                        if path:

                            ux, uy = movement.get_coords(uid)
                            hx = t['hex_x'](ux, uy, S)
                            hy = t['hex_y'](ux, uy, S)
                            data = engine.containers[cur_uid].data[graphics.id]
                            animation_name = data['animation']['original_name']

                            engine.push_event(UpdateMapLayerEvent(texture=m.layers['Surfaces'][uy][ux], x1=ux, y1=uy, layer='UnitsTextures'))


                            for i in range(1, len(path)):
                                prev_x = t['hex_x'](path[i-1][0], path[i-1][1], S)
                                prev_y = t['hex_y'](path[i-1][0], path[i-1][1], S)
                                cur_x = t['hex_x'](path[i][0], path[i][1], S)
                                cur_y = t['hex_y'](path[i][0], path[i][1], S)


                                renderer.animate(animation_name, prev_x, prev_y, cur_x, cur_y, step=1)

                            movement.move(cur_uid, int(map_x-ux), int(map_y-uy))

                            ap = attributes.get_attribute(uid, 'action_points')
                            attributes.set_attribute(uid, 'action_points', ap-len(path))

                            engine.push_event(PrerenderMapLayerEvent(layer='UnitsTextures'))

                            # ~graphics.prerender_map_layer(layer='UnitsTextures')


            # ~elif type(event) is sf.MouseMoveEvent:
                # ~x, y = sf.Mouse.get_position(window)
                # ~window_size_x, window_size_y = window.size
                # ~cx, cy = window.view.center
                # ~dcx = 0
                # ~dcy = 0
                # ~nx, ny = nearest(x, y, S, t)
                # ~engine.push_event(ShowWayEvent(x1=nx, y1=ny))

            elif type(event) is sf.KeyEvent:
                if event.pressed:
                    code = event.code

                    cx, cy = window.view.center
                    dcx = 0
                    dcy = 0

                    if code==sf.Keyboard.DOWN:
                        dcy = 10
                    elif code==sf.Keyboard.UP:
                        dcy = -10
                    if code==sf.Keyboard.RIGHT:
                        dcx = 10
                    elif code==sf.Keyboard.LEFT:
                        dcx = -10
                    if dcx or dcy:
                        window.view.center = (cx+dcx, cy+dcy)

                    if code==sf.Keyboard.SPACE:

                        for objid in attributes.containers:
                            print("OBJID:", objid)
                            max_action_points = attributes.get_attribute(objid, 'max_action_points')
                            attributes.set_attribute(objid, 'action_points', max_action_points)
                        
                        print(m.layers['Units'])
                        
                        engine.push_event(AIUpdateEvent())

        while engine.events_queue:
        # ~for iii in range(len(engine.events_queue)):

            event = engine.poll_event()

            # ~print(">>>EVENT TYPE IS:", type(event))

            if type(event) is UpdateSceneEvent:

                # ~layers_order = event.layers_order
                # ~sprites = graphics.sprites_container.data[graphics.id]
                # ~for l in layers_order:
                    # ~renderer.draw_map_layer(layer=l)
                # ~print(">>>EVENT:", event)
                graphics.update(event)
                # ~print(">>>EVENT:", event)
                renderer.update(event)
                
            elif type(event) is ClearCanvasEvent:

                if 'color' in event.__dict__:
                    color = event.color
                else:
                    color = sf.Color(215, 170, 0, 128)

                window.clear(color)

            elif type(event) is DisplayEvent:

                window.display()

            elif type(event) is DrawStaticEvent:

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
                    rectangle = sf.Rectangle((0, 0), (S, S))

                renderer.draw_static(name, x1=x1, y1=y1, anchor=anchor, rectangle=rectangle)
                window.display()

            elif type(event) is OutlineUnitEvent:

                uid = event.uid

                unit = engine.containers[uid]

                ux = unit.data[movement.id]['x']
                uy = unit.data[movement.id]['y']

                # ~print('UX, UY:', ux, uy)

                hx = t['hex_x'](ux, uy, S)
                hy = t['hex_y'](ux, uy, S)

                # ~print('hx, hy:', hx, hy)


                circle.position = (hx, hy)
                window.draw(circle)

            elif type(event) is ShowPossibleWaysEvent:

                uid = event.uid

                action_points = attributes.get_attribute(uid, 'action_points')

                if not action_points is None and action_points>=0:

                    ux, uy = movement.get_coords(uid)

                    possible_cells, graph = possible_ways(m, ux, uy, action_points)
                    possible_cells.pop(0)

                    for j in possible_cells:
                        for i in j:
                            circle1.position = (t['hex_x'](i[0], i[1], S), t['hex_y'](i[0], i[1], S))
                            window.draw(circle1)

            elif type(event) is ShowWayEvent:

                x1 = event.x1
                y1 = event.y1

                cur_x = x1
                cur_y = y1

                path = []

                while any([(cur_x, cur_y) in i for i in possible_cells]):
                    for i in graph:
                        # ~print("GRAPH[I]:", i, graph[i])
                        if (cur_x, cur_y) in graph[i]:
                            path.append((cur_x, cur_y))
                            cur_x, cur_y = i
                            continue
                            # ~break

                path.reverse()

                # ~print("PATH:", path)

                for i in path:
                    circle2.position = (t['hex_x'](i[0], i[1], S), t['hex_y'](i[0], i[1], S))
                    window.draw(circle2)


            elif type(event) is PrerenderMapLayerEvent:
                layer = event.layer
                graphics.prerender_map_layer(layer=layer)

            elif type(event) is UpdateMapLayerEvent:

                x1 = event.x1
                y1 = event.y1
                texture = event.texture
                layer = event.layer

                graphics.update_map_layer(x1=x1, y1=y1, texture=texture, layer=layer)

            elif type(event) is ShowMessageEvent:

                message = event.message

                if 'size' in event.__dict__:
                    size = event.size
                else:
                    size = 16

            elif type(event) is AIUpdateEvent:
                ai.update()
                graphics.prerender_map_layer(layer='UnitsTextures')

            elif type(event) is AskEvent:

                # ~message = event.message
                # ~answers = event.answers
                conv = event.conversation
                # ~lastanswer = conv['.answers'][-1]
                lastanswer = conv['.lastanswer']
                if lastanswer in conv:
                    message = conv[lastanswer]['message']
                    answers = conv[lastanswer]['answers']

                    if 'size' in event.__dict__:
                        size = event.size
                    else:
                        size = 16

                    answer = ask(window, engine, message, size, answers=answers)
                    
                    # ~print("ANSWER:", answer)

                    if not answer is None:
                        conv['.lastanswer'] = answer
                    else:
                        engine.push_event(AskEvent(conversation=conv))
                        engine.push_event(DisplayEvent())
                        print("ASK 2")
                    # ~engine.push_event(ClearCanvasEvent())
                    if answer in conv:
                        engine.push_event(AskEvent(conversation=conv))
                        engine.push_event(DisplayEvent())
                        print("ASK 1")

        current_time = clock.elapsed_time.milliseconds

        delta_time = current_time - last_time

        # ~print(">>>DELAY:", TIMING-delta_time%TIMING)

        sf.sleep(sf.milliseconds(TIMING-delta_time%TIMING))

        # ~last_time = current_time

