#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')

import sfml as sf

from math import sqrt

sign = lambda x: 1 if x>0 else -1 if x<0 else 0

DEFAULTCONTAINERSIDMANAGER = lambda x: id(x)
DEFAULTCOMPONENTSIDMANAGER = lambda x: type(x)

#HORIZ1 = [0, 1, 0, 0]
#VERT1 = [0, 0, 0, 1]
#HORIZ2 = [1, 0, 0, 0]
#VERT2 = [0, 0, 1, 0]

A = lambda s: sqrt(3)*s
B = lambda s: 2*s
H = lambda s: s/2
R = lambda s: sqrt(3)/2*s

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
          'x': lambda x, y, s: x//(1.5*s),
          'y': lambda x, y, s: (y + R(s)*((x//(1.5*s))%2-1))//A(s)
          }

VERT_0 = {'dx': lambda y: (0, +1, +1, 0, -1, -1),
          'dy': lambda x: (-1, (x%2-1), (x%2), +1, (x%2), (x%2-1)),
          'shift_x': 2,
          'shift_y': -1,
          'hex_x': lambda x, y, s: (H(s)+s)*x+s,# -H(s),
          'hex_y': lambda x, y, s: A(s)*y+R(s)*(x%2)+R(s),
          'x': lambda x, y, s: x//(1.5*s),
          'y': lambda x, y, s: (y - R(s)*((x//(1.5*s))%2-1))//A(s)
          }

HORIZ_0 = {'dx': lambda y: ((y%2-1), (y%2), +1, (y%2), (y%2-1), -1),
           'dy': lambda x: (-1, -1, 0, 1, 1, 0),
           'shift_x': -1,
           'shift_y': 1,
           'hex_x': lambda x, y, s: A(s)*x+R(s)*(y%2)+R(s),
           'hex_y': lambda x, y, s: (H(s)+s)*y+s,# -H(s),
           'x': lambda x, y, s: (x - R(s)*(y//(1.5*s)%2))//A(s),
           'y': lambda x, y, s: y//(1.5*s)
           }

HORIZ_1 = {'dx': lambda y: (-1*(y%2), -1*(y%2-1), +1, -1*(y%2-1), -1*(y%2), -1),
           'dy': lambda x: (-1, -1, 0, +1, +1, 0),
           'shift_x': -1,
           'shift_y': 2,
           'hex_x': lambda x, y, s: A(s)*x-R(s)*(y%2-1)+R(s),
           'hex_y': lambda x, y, s: (H(s)+s)*y+s,# -H(s),
           'x': lambda x, y, s: (x - R(s)*(y//(1.5*s)%2+1))//A(s),
           'y': lambda x, y, s: y//(1.5*s)
           }

SQUARE = {'dx': lambda y: (0, +1, 0, -1),
          'dy': lambda x: (-1, 0, +1, 0),
          'shift_x': -1,
          'shift_y': -1,
          'hex_x': lambda x, y, s: H(s)+s*x,
          'hex_y': lambda x, y, s: H(s)+s*y,
          'x': lambda x, y, s: x//s,
          'y': lambda x, y, s: y//s
          }


def nearest(x, y, s, t):

    x1 = t['x'](x, y, s) # approximately x
    y1 = t['y'](x, y, s) # approximately y

    dx = t['dx'](y1)+(0,) # cells around
    dy = t['dy'](x1)+(0,) # cells around

    xl = [t['hex_x'](x1+dx[i], y1+dy[i], 40) for i in range(len(dx))] # list of neighbours coords
    yl = [t['hex_y'](x1+dx[i], y1+dy[i], 40) for i in range(len(dy))] # list of neighbours coords

    r = [sqrt((x-xl[i])**2+(y-yl[i])**2) for i in range(len(dx))] # list of radius

    i = r.index(min(r))

    return(int(x1+dx[i]), int(y1+dy[i]))


def pathfind(m, x1, y1, x2, y2, window):

    if x1<0 or x2<0 or y1<0 or y2<0 or x1>m.X or x2>m.X or y1>m.Y or y2>m.Y:
        return [(0,0), ]

    if m.layers['Walk'][y2][x2] == -1:
        return [(0,0), ]

    t = m.type

    checked = set()

    cur_x = x1
    cur_y = y1

    cur_deep = 1

    queue = [(cur_x, cur_y), (-1, -1)]

    m1 = [[0 for i in range(m.X)] for j in range(m.Y)]

    # ~ print('>>>BUILDING MAP')
    # ~ print('X2, Y2:', x2, y2)
    while queue and not ((x2, y2) in checked):
        # ~ while not(queue and queue[0]==(-1, -1)):
        while queue:

            cur_x, cur_y = queue.pop(0)

            if cur_x==cur_y==-1:
                if queue:
                    queue.append((-1, -1))
                    cur_deep += 1
                    # ~ print('CUR_DEEP:', cur_deep)
                    continue
                else:
                    break

            dx = t['dx'](cur_y)
            dy = t['dy'](cur_x)

            dxy = [(dx[i], dy[i]) for i in range(len(dx))]

            for i in dxy:
                if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):
                    if not m.layers['Walk'][cur_y+i[1]][cur_x+i[0]] == -1:
                        if not((cur_x+i[0], cur_y+i[1]) in checked or (cur_x+i[0], cur_y+i[1]) in queue):
                            m1[cur_y+i[1]][cur_x+i[0]] += cur_deep
                            queue.append((cur_x+i[0], cur_y+i[1]))
                    else:
                        m1[cur_y+i[1]][cur_x+i[0]] = -1
                        checked.add((cur_x+i[0], cur_y+i[1]))

            checked.add((cur_x, cur_y))

        # ~ queue.append((-1, -1))
        # ~ cur_deep += 1
        # ~ print('CUR_DEEP:', cur_deep)
        # ~ print('QUEUE:', queue)

        if queue and queue[0]==(-1, -1):
            queue.pop(0)

    if not ((x2, y2) in checked):
        print('TARGET UNREACHABLE')
        return [(0, 0),]

    path = [(x2, y2),]

    cur_x = x2
    cur_y = y2

    # ~ font = sf.Font.from_file('/usr/share/fonts/truetype/msttcorefonts/arial.ttf')

    # ~ for i in range(m.Y):
        # ~ for j in range(m.X):
            # ~ text = sf.Text(str((j, i))+'\n'+str(m1[i][j]), font, 14)
            # ~ text.color = sf.Color.RED
            # ~ text.origin = (0.5, 0.5)
            # ~ text.position=(t['hex_x'](j, i, 40), t['hex_y'](j, i, 40))
            # ~ window.draw(text)
            # ~ window.display()

    # ~ print(m1)
    # ~ print('>>>SEARCHING PATH')

    nm = m1[y2][x2]
    cur_nm = nm

    while not((x1, y1) in path):

        cur_x, cur_y = path[-1]

        # ~ print('CUR_X, CUR_Y:', cur_x, cur_y)

        dx = t['dx'](cur_y)
        dy = t['dy'](cur_y)

        dxy = [(dx[i], dy[i]) for i in range(len(dx))]

        for i in dxy:
            if not(cur_x+i[0]<0 or cur_x+i[0]>=m.X or cur_y+i[1]<0 or cur_y+i[1]>=m.Y):
                if m1[cur_y+i[1]][cur_x+i[0]] < m1[cur_y][cur_x] and not((cur_x+i[0], cur_y+i[1]) in path):
                    if not(m1[cur_y+i[1]][cur_x+i[0]]==-1):
                        # ~ if m1[cur_y+i[1]][cur_x+i[0]] < nm:
                            # ~ nm = m1[cur_y+i[1]][cur_x+i[0]]
                            # ~ nn = (cur_x+i[0], cur_y+i[1])
                        path.append((int(cur_x+i[0]), int(cur_y+i[1])))
                        break
        # ~ path.append(nn)


    return path

if __name__ == '__main__':

    print(VERT_1['dy'](0), VERT_1['dy'](1))
    print(VERT_0['dy'](0), VERT_0['dy'](1))
    print(HORIZ_1['dx'](0), HORIZ_1['dx'](1))
    print(HORIZ_0['dx'](0), HORIZ_0['dx'](1))