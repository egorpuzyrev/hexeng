#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
sys.path.append('../')

#~ import sfml as sf
#~ from sfml import sf

# ~from components.components import *
# ~from models.models import *
# ~from engine.engine import *
from events.events import *

# ~from engine.engine import Engine
# ~from models.unit import Unit
# ~from models.map import Map
# ~from models.container import Container

# ~from components.renderer import Renderer


from math import sqrt

import json

import sfml as sf


sign = lambda x: 1 if x>0 else -1 if x<0 else 0

radius = lambda dx, dy: sqrt(dx**2+dy**2)

# ~zoom_coeff = lambda c, d: (c**2*(d+1)+1)/(2*c)
zoom_coeff = lambda c, d: (d+(c**2+1)/(c**2-1))/(2*c/(c**2-1))


DEFAULTCONTAINERSIDMANAGER = lambda x: id(x)
DEFAULTCOMPONENTSIDMANAGER = lambda x: type(x)

#HORIZ1 = [0, 1, 0, 0]
#VERT1 = [0, 0, 0, 1]
#HORIZ2 = [1, 0, 0, 0]
#VERT2 = [0, 0, 1, 0]

S = 80
A = lambda s: sqrt(3)*s
B = lambda s: 2*s
H = lambda s: s/2
R = lambda s: sqrt(3)/2*s

TIMING = 40

SCROLLZONE = 20

# ======================================================================
# VERT_1 = { - typename
#          'dx': dx in array
#          'dy': dy in array
#          'shift_x': number of shifted column, deprecated
#          'shift_y': number of shifted row, deprecated
#          'hex_x': returns coords on canvas depends on position in array
#          'hex_y': returns coords on canvas depends on position in array
#          'x': returns approximately coords in array depends on mouse position
#          'y': returns approximately coords in array depends on mouse position
#          }
# ======================================================================

VERT_1 = {'dx': lambda y: (0, +1, +1, 0, -1, -1),
          'dy': lambda x: (-1, -1*(x%2), -1*(x%2-1), +1, -1*(x%2-1), -1*(x%2)),
          'shift_x': 1,
          'shift_y': -1,
          'hex_x': lambda x, y, s: (H(s)+s)*x+s,# -H(s),
          'hex_y': lambda x, y, s: A(s)*y-R(s)*(x%2-1)+R(s),
          'x': lambda x, y, s: int(x//(1.5*s)),
          'y': lambda x, y, s: int((y + R(s)*((x//(1.5*s))%2-1))//A(s))
          }

VERT_0 = {'dx': lambda y: (0, +1, +1, 0, -1, -1),
          'dy': lambda x: (-1, (x%2-1), (x%2), +1, (x%2), (x%2-1)),
          'shift_x': 2,
          'shift_y': -1,
          'hex_x': lambda x, y, s: (H(s)+s)*x+s,# -H(s),
          'hex_y': lambda x, y, s: A(s)*y+R(s)*(x%2)+R(s),
          'x': lambda x, y, s: int(x//(1.5*s)),
          'y': lambda x, y, s: int((y - R(s)*((x//(1.5*s))%2-1))//A(s))
          }

HORIZ_0 = {'dx': lambda y: ((y%2-1), (y%2), +1, (y%2), (y%2-1), -1),
           'dy': lambda x: (-1, -1, 0, 1, 1, 0),
           'shift_x': -1,
           'shift_y': 1,
           'hex_x': lambda x, y, s: A(s)*x+R(s)*(y%2)+R(s),
           'hex_y': lambda x, y, s: (H(s)+s)*y+s,# -H(s),
           'x': lambda x, y, s: int((x - R(s)*(y//(1.5*s)%2))//A(s)),
           'y': lambda x, y, s: int(y//(1.5*s))
           }

HORIZ_1 = {'dx': lambda y: (-1*(y%2), -1*(y%2-1), +1, -1*(y%2-1), -1*(y%2), -1),
           'dy': lambda x: (-1, -1, 0, +1, +1, 0),
           'shift_x': -1,
           'shift_y': 2,
           'hex_x': lambda x, y, s: A(s)*x-R(s)*(y%2-1)+R(s),
           'hex_y': lambda x, y, s: (H(s)+s)*y+s,# -H(s),
           'x': lambda x, y, s: int((x - R(s)*(y//(1.5*s)%2+1))//A(s)),
           'y': lambda x, y, s: int(y//(1.5*s))
           }

SQUARE = {'dx': lambda y: (0, +1, 0, -1),
          'dy': lambda x: (-1, 0, +1, 0),
          'shift_x': -1,
          'shift_y': -1,
          'hex_x': lambda x, y, s: H(s)+s*x,
          'hex_y': lambda x, y, s: H(s)+s*y,
          'x': lambda x, y, s: int(x//s),
          'y': lambda x, y, s: int(y//s)
          }

MAP_TYPES = {
    'VERT_1': VERT_1,
    'HORIZ_1': HORIZ_1,
    'VERT_0': VERT_0,
    'HORIZ_0': HORIZ_0,
    'SQUARE': SQUARE,
    }

def nearest(x, y, s, t):

    x1 = t['x'](x, y, s) # approximately x
    y1 = t['y'](x, y, s) # approximately y

    dx = t['dx'](y1)+(0,) # cells around
    dy = t['dy'](x1)+(0,) # cells around

    xl = [t['hex_x'](x1+dx[i], y1+dy[i], s) for i in range(len(dx))] # list of neighbours coords
    yl = [t['hex_y'](x1+dx[i], y1+dy[i], s) for i in range(len(dy))] # list of neighbours coords

    r = [sqrt((x-xl[i])**2+(y-yl[i])**2) for i in range(len(dx))] # list of radius

    i = r.index(min(r))

    return(int(x1+dx[i]), int(y1+dy[i]))


def pathfind(m, x1, y1, x2, y2, layer='Walk'):
    """
    m - Map object
    layer - layer for pathfinding
    returns path from x2, y2 to x1, y1
    """

    print(">>>STARTED PATHFIND")

    if x1<0 or x2<0 or y1<0 or y2<0 or x1>m.X or x2>m.X or y1>m.Y or y2>m.Y:
        return [(x1,y1), ]

    if m.layers['Walk'][y2][x2] == -1:
        return [(x1,y1), ]

    t = m.type

    checked = set()

    cur_x = x1
    cur_y = y1

    cur_deep = 1

    queue = [(cur_x, cur_y), (-1, -1)]

    m1 = [[0 for i in range(m.X)] for j in range(m.Y)]


    # ~while queue and not ((x2, y2) in checked):
    while queue and not ((x2, y2) in checked):
        print("while queue and not ((x2, y2) in checked):")
        while queue:
            print("while queue:")

            cur_x, cur_y = queue.pop(0)

            if cur_x==cur_y==-1:
                if queue:
                    queue.append((-1, -1))
                    cur_deep += 1
                    continue
                else:
                    break

            dx = t['dx'](cur_y)
            dy = t['dy'](cur_x)

            dxy = [(dx[i], dy[i]) for i in range(len(dx))]

            for i in dxy:
                print("for i in dxy:")

                icur_x = int(cur_x+i[0])
                icur_y = int(cur_y+i[1])

                if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):
                    print("if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):")
                    if not m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] == -1:
                    # ~if not m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] <= -1:
                    # ~if m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] >= 0:
                        print("if m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] >= 0:")
                        # ~print(i)
                        # ~print(m.layers['Walk'])
                        if not((cur_x+i[0], cur_y+i[1]) in checked or (cur_x+i[0], cur_y+i[1]) in queue):
                            print("if not((cur_x+i[0], cur_y+i[1]) in checked or (cur_x+i[0], cur_y+i[1]) in queue):")
                            m1[icur_y][icur_x] += cur_deep
                            queue.append((icur_x, icur_y))
                        print(i)
                    else:
                        print("else if m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] >= 0:")
                        m1[icur_y][icur_x] = -1
                        checked.add((icur_x, icur_y))

            checked.add((cur_x, cur_y))
            print("checked.add((cur_x, cur_y))")


        if queue and queue[0]==(-1, -1):
            print("if queue and queue[0]==(-1, -1):")
            queue.pop(0)

    if not ((x2, y2) in checked):
        print("if not ((x2, y2) in checked):")

        # ~return [(0, 0),]
        return [(x1, y1),]

    path = [(x2, y2),]

    cur_x = x2
    cur_y = y2

    nm = m1[y2][x2]
    cur_nm = nm

    while not((x1, y1) in path):
        print("while not((x1, y1) in path):")

        cur_x, cur_y = path[-1]


        dx = t['dx'](cur_y)
        dy = t['dy'](cur_y)



        dxy = [(dx[i], dy[i]) for i in range(len(dx))]

        count = 0
        for i in dxy:
            print("for i in dxy:")

            icur_x = int(cur_x+i[0])
            icur_y = int(cur_y+i[1])

            if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):
                print("if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):")
                if m1[cur_y+i[1]][cur_x+i[0]] < m1[cur_y][cur_x] and not((cur_x+i[0], cur_y+i[1]) in path):
                    print("if m1[cur_y+i[1]][cur_x+i[0]] < m1[cur_y][cur_x] and not((cur_x+i[0], cur_y+i[1]) in path):")
                    # ~if not(m1[cur_y+i[1]][cur_x+i[0]]==-1):
                    if (m1[cur_y+i[1]][cur_x+i[0]]>=0):
                        print("if not(m1[cur_y+i[1]][cur_x+i[0]]==-1):")
                        path.append((icur_x, icur_y))
                        break
            
            if not(path[-1]==(icur_x, icur_y)):
                count += 1
                
        if count==len(dxy):
            break

    print(">>>FINISHED PATHFIND")
    print(">>>PATH:", path)
    return path



def possible_ways(m, x1, y1, deep=1, layer='Walk'):

    print(">>>STARTED POSSIBLE WAYS")

    t = m.type

    checked = set()

    cur_x = x1
    cur_y = y1

    cur_deep = 1

    queue = [(cur_x, cur_y), (-1, -1)]

    m1 = [[0 for i in range(m.X)] for j in range(m.Y)]

    path = [[] for i in range(deep+1)]
    path[0].append((x1, y1))

    neighbours = {}

    while cur_deep<=deep and (cur_deep<m.X and cur_deep<m.Y):
        while queue and cur_deep<=deep:

            cur_x, cur_y = queue.pop(0)

            if cur_x==cur_y==-1:
                if queue:
                    queue.append((-1, -1))
                    cur_deep += 1

                    continue
                else:
                    break

            neighbours[(cur_x, cur_y)] = []

            dx = t['dx'](cur_y)
            dy = t['dy'](cur_x)

            dxy = [(dx[i], dy[i]) for i in range(len(dx))]

            for i in dxy:

                icur_x = int(cur_x+i[0])
                icur_y = int(cur_y+i[1])

                if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):
                    # ~if not m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] == -1:
                    # ~if not m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] <= -1:
                    if m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] >= 0:
                        # ~print(m.layers['Walk'])
                        if not((cur_x+i[0], cur_y+i[1]) in checked or (cur_x+i[0], cur_y+i[1]) in queue):

                            neighbours[(cur_x, cur_y)].append((icur_x, icur_y))

                            m1[icur_y][icur_x] += cur_deep
                            queue.append((icur_x, icur_y))
                            path[cur_deep].append((icur_x, icur_y))
                    else:
                        m1[icur_y][icur_x] = -1
                        checked.add((icur_x, icur_y))

            checked.add((cur_x, cur_y))

    print(">>>FINISHED POSSIBLE WAYS")

    return path, neighbours




def show_message(w, message, size=16, dx=0, dy=0):

    cx, cy = w.size

    cx /= 2
    cy /= 2

    cx += dx
    cy += dy

    font = sf.Font.from_file('fonts/LiberationSans-Regular.ttf')

    text = sf.Text(str(message), font, size)
    text.position = (cx, cy)
    text.origin = (text.local_bounds.width/2, text.local_bounds.height/2)

    bg = sf.RectangleShape()
    bg.size = (200, 100)
    bg.origin = (100, 50)
    bg.outline_thickness = 5
    bg.outline_color = sf.Color(200, 200, 200, 255)
    bg.fill_color = sf.Color(50, 50, 200, 150)

    bg.position = (cx, cy)

    w.draw(bg)
    w.draw(text)
    w.display()

    done = 0

    while done == 0:
        for event in w.events:
            if type(event) == sf.MouseButtonEvent:
                if event.button == sf.Mouse.RIGHT and event.pressed:
                    done = 1

font = sf.Font.from_file('fonts/LiberationSans-Regular.ttf')
def ask(w, e, message, size=16, dx=0, dy=0, answers=[]):

    cx, cy = w.size

    cx /= 2
    cy /= 2

    cx += dx
    cy += dy

    
    # ~font = sf.Font.from_file('/usr/share/fonts/truetype/msttcorefonts/arial.ttf')

    text = sf.Text(str(message), font, size)
    text.position = (cx, cy)
    text.origin = (text.local_bounds.width/2, text.local_bounds.height/2)

    l = max([len(i) for i in message.split('\n')])

    bg = sf.RectangleShape()
    # ~bg.size = (200, 100)
    # ~bg.origin = (100, 50)
    bg.size = (size//2*(l+1), 100)
    bg.origin = (size//4*(l+1), 50)
    bg.outline_thickness = 5
    bg.outline_color = sf.Color(200, 200, 200, 255)
    bg.fill_color = sf.Color(50, 50, 200, 200)

    bg.position = (cx, cy)

    bg1 = sf.RectangleShape()
    bg1.size = (200, len(answers)*20+20)
    bg1.origin = (100, 0)# len(answers)*10+10)
    bg1.outline_thickness = 5
    bg1.outline_color = sf.Color(100, 150, 150, 255)
    bg1.fill_color = sf.Color(150, 200, 50, 200)

    bg1.position = (cx, cy+55)
    
   
    # ~print('bg1.global_bounds:', bg1.global_bounds)

    texts = []

    for i in enumerate(answers):
        texts.append(sf.Text(str(i[1]), font, size))
        texts[-1].position = (cx, cy+70+20*i[0])
        texts[-1].origin = (texts[-1].local_bounds.width/2, texts[-1].local_bounds.height/2)

    w.draw(bg)
    w.draw(text)

    w.draw(bg1)
    for i in texts:
        w.draw(i)


    # ~w.display()

    done = 0
    answer = -1

    # ~while done == 0:
    # ~engine.push_event(UpdateSceneEvent())
    for event in w.events:
        if type(event) == sf.MouseButtonEvent:
            if event.button == sf.Mouse.LEFT and event.pressed:
                x, y = w.map_pixel_to_coords(event.position)
                for i in enumerate(texts):
                    rect = i[1].global_bounds
                    cox, coy = rect.position
                    dox, doy = rect.size
                    
                    if cox<=x<=cox+dox and coy<=y<=coy+doy:
                                                
                        answer = answers[i[0]]
                        
                        done = 1
                        print(answer)
                        
                        e.push_event(ClearCanvasEvent())
                        e.push_event(UpdateSceneEvent(layers_order=['Surfaces', 'Buildings', 'UnitsTextures']))
                        e.push_event(DisplayEvent())
                        
                        return answer
        # ~done = 1

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS",
            os.path.abspath(".")
        ),
        relative
    )


if __name__ == '__main__':

    print(VERT_1['dy'](0), VERT_1['dy'](1))
    print(VERT_0['dy'](0), VERT_0['dy'](1))
    print(HORIZ_1['dx'](0), HORIZ_1['dx'](1))
    print(HORIZ_0['dx'](0), HORIZ_0['dx'](1))
