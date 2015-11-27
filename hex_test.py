#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt
import tkinter as tk
from PIL import Image, ImageTk

def renew_coords(event):
    
    x = (event.x)//(h)
    y = (event.y)//r
    
    rx = x//3
    if rx%2:
        ry = (y-1)//2
    else:
        ry = y//2
    
    dx = event.x - x*h
    dy = event.y - y*r


    if not x%3:
        if (x//3)%2:
            if not y%2:
                if dy>dx*sqrt(3):
                    rx -= 1
                    ry += 1
            else:
                if dy<r-dx*sqrt(3):
                    rx -= 1
        else:
            if not y%2:
                if dy<r-dx*sqrt(3):
                    rx -= 1
                    ry -= 1
            else:
                if dy>dx*sqrt(3):
                    rx -= 1


    status.textvar.set("dec: %d:%d\tdx: %d dy: %d\trx: %d ry: %d\t\tsqx: %d sqy: %d" %(event.x, event.y, dx, dy, rx, ry, x, y))


def draw_tank(event):
    
    x = (event.x)//(h)
    y = (event.y)//r
    
    rx = x//3
    if rx%2:
        ry = (y-1)//2
    else:
        ry = y//2
    
    dx = event.x - x*h
    dy = event.y - y*r


    if not x%3:
        if (x//3)%2:
            if not y%2:
                if dy>dx*sqrt(3):
                    rx -= 1
                    ry += 1
            else:
                if dy<r-dx*sqrt(3):
                    rx -= 1
        else:
            if not y%2:
                if dy<r-dx*sqrt(3):
                    rx -= 1
                    ry -= 1
            else:
                if dy>dx*sqrt(3):
                    rx -= 1
    
    img_x = (rx+1)*(s+h) - h
    img_y = (ry+1)*a - r if not(rx%2) else (ry+1)*a
    
    global last
    last = canvas.create_image(img_x, img_y, image=tank)


def move_tank(event):
    
    x = (event.x)//(h)
    y = (event.y)//r
    
    rx = x//3
    if rx%2:
        ry = (y-1)//2
    else:
        ry = y//2
    
    dx = event.x - x*h
    dy = event.y - y*r


    if not x%3:
        if (x//3)%2:
            if not y%2:
                if dy>dx*sqrt(3):
                    rx -= 1
                    ry += 1
            else:
                if dy<r-dx*sqrt(3):
                    rx -= 1
        else:
            if not y%2:
                if dy<r-dx*sqrt(3):
                    rx -= 1
                    ry -= 1
            else:
                if dy>dx*sqrt(3):
                    rx -= 1
    
    img_x = (rx+1)*(s+h) - h
    img_y = (ry+1)*a - r if not(rx%2) else (ry+1)*a
    
    global last
    # ~ last = canvas.create_image(img_x, img_y, image=tank)
    canvas.coords(last, img_x, img_y)

w = tk.Tk()
w.geometry("640x480")

canvas = tk.Canvas(w, bg="white")
# ~ canvas.pack()
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

status = tk.Label(w, anchor=tk.W, text="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# ~ status.pack(fill=tk.X)
status.place(relx=0, rely=1, relwidth=1, y=-20)

status.textvar = tk.StringVar()
status.textvar.set("qaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
status.config(textvariable = status.textvar)


canvas.bind("<Motion>", renew_coords)
canvas.bind("<Button-1>", draw_tank)
canvas.bind("<Button-3>", move_tank)

tank = ImageTk.PhotoImage(Image.open('/home/egor/Pictures/game/Battle_City_Tank_Player2.png'))



s=40.0
h=0.5*s
r=sqrt(3)*0.5*s
b=2.0*s
a=sqrt(3)*s

for i in range(20):
    for j in range(20):

        # ~ canvas.create_line(j*h, 0, j*h+2000, (j*h+2000)*sqrt(3)/2, fill="green")

        # ~ canvas.create_line(0, r*i+r, 2000, r*i+r, fill="blue")
        # ~ canvas.create_line(j*(h), 0, j*(h), 2000, fill="blue")

        if not j%2:
            # ~ canvas.create_line(j*2*s, i*2*s+s, j*2*s+s, i*2*s+s)
            x = j*(s+h)
            y = i*a
            # ~ canvas.create_polygon(x, y+r, x+h, y, x+s+h, y, x+b, y+r, x+s+h, y+a, x+h, y+a, x, y+r, fill="white", outline="black")
            canvas.create_polygon(x, y+r, x+h, y, x+s+h, y, x+b, y+r, x+s+h, y+a, x+h, y+a, x, y+r, fill="white", outline="black")
            # ~ canvas.create_polygon(x, y+r, x+h, y, x+s+h, y, x+b, y+r, x, y+r, fill="white", outline="black")
            
        else:
            x = j*(s+h)
            y = i*a+r
            canvas.create_polygon(x, y+r, x+h, y, x+s+h, y, x+b, y+r, x+s+h, y+a, x+h, y+a, x, y+r, fill="white", outline="red")
            # ~ canvas.create_polygon(x, y+r, x+h, y, x+s+h, y, x+b, y+r, x+s+h, y+a, x+h, y+a, x, y+r, fill="white", outline="red")
# ~ canvas.create_line(10, 10, 2000, 2000*sqrt(3), fill="green")
w.mainloop()
