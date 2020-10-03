from window import Screen
from settings import *
from tkinter import *
import numpy
import keyboard
import time


screen = Screen(WINDOW_WIDTH,WINDOW_HEIGTH)
screen = screen.screen

canvas = Canvas(screen, width=WINDOW_WIDTH,height=WINDOW_HEIGTH)
canvas.pack()

bounds_x = [100, 620]
bounds_y = [25, 620]

corners = [[100,25],[620,25],[620,620],[100,620]]

canvas.create_line(100,25,620,25,620,620,100,620,100,25)

people = []
delimiter_x = 15
delimiter_y = 15

for i in range(0,30):
    start_x = numpy.random.randint(100,618)
    start_y = numpy.random.randint(25,618)
    if(start_x+delimiter_x >= 618):
        start_x = start_x - delimiter_x
    if(start_y+delimiter_y >= 618):
        start_y = start_y - delimiter_y
    ball = canvas.create_oval(start_x, start_y,start_x+delimiter_x, start_y+delimiter_y, outline="black",
                fill="snow", width=2)
    people.append(ball)
    
for p in people:
    print('ID:{},coordinates: {}'.format(p,canvas.coords(p)))


infected_id = numpy.random.randint(people[0],people[len(people)-1])
print(infected_id)
canvas.itemconfig(infected_id,fill="red")

def motion(event):
    x, y = event.x, event.y
    position.configure(text='{},{}'.format(x,y))

position = Label(screen,text = '0,0')
canvas.create_window(60,20,window = position)

screen.bind('<Motion>', motion)

loop = False
xspeed,yspeed = [0,0],[0,0]
for _ in range(len(people)):
    move_x,move_y = 0,0
    while(move_x == 0 and move_y == 0):
        move_x = numpy.random.randint(-10,10)
        move_y = numpy.random.randint(-10,10)
    xspeed.append(move_x)
    yspeed.append(move_y)

while 1:
    if(loop):
        for p in people:
            x1,y1,x2,y2 = canvas.coords(p)
            x1=int(x1)
            x2=int(x2)
            y1=int(y1)
            y2=int(y2)
            print('x1:{},x2:{},y1:{},y2:{}'.format(x1,x2,y1,y2))
            if(x1+xspeed[p] < bounds_x[0]):
                if(y1+yspeed[p] < bounds_y[0]):
                    canvas.move(p,bounds_x[0]-x1,bounds_y[0]-y1)
                    yspeed[p] *= -1
                elif(y2+yspeed[p]> bounds_y[1]):
                    canvas.move(p,bounds_x[0]-x1,bounds_y[1]-y2)
                    yspeed[p] *= -1
                else:    
                    canvas.move(p,bounds_x[0]-x1,yspeed[p])
                xspeed[p] *= -1
                #canvas.move(infected_id,move_x,move_y)
            elif(x2+xspeed[p] > bounds_x[1]):
                if(y1+yspeed[p] < bounds_y[0]):
                    canvas.move(p,bounds_x[1]-x2,bounds_y[0]-y1)
                    yspeed[p] *= -1
                elif(y2+yspeed[p] > bounds_y[1]):
                    canvas.move(p,bounds_x[1]-x2,bounds_y[1]-y2)
                    yspeed[p] *= -1
                else:    
                    canvas.move(p,bounds_x[1]-x2,yspeed[p])
                xspeed[p] *= -1
            else:
                if(y1+yspeed[p] < bounds_y[0]):
                    canvas.move(p,xspeed[p],bounds_y[0]-y1)
                    yspeed[p] *= -1
                elif(y2+yspeed[p] > bounds_y[1]):
                    canvas.move(p,xspeed[p],bounds_y[1]-y2)
                    yspeed[p] *= -1
                else:    
                    canvas.move(p,xspeed[p],yspeed[p])
        

    if keyboard.is_pressed('q'):
        if(loop == True):
            loop = False
        else:
            loop = True
    if keyboard.is_pressed('e'):
        break
    
    time.sleep(0.05)
    screen.update()
