from window import Screen
from settings import *
from tkinter import *
from math import *
import numpy
import keyboard
import time

class human(object):
    def __init__(self,color,x,y):
        self.color = color
        self.x = x
        self.y = y
    
    def setPosition(self,x,y):
        self.x = x
        self.y = y
        return "done"

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPosition(self):
        return self.x, self.y

screen = Screen(WINDOW_WIDTH,WINDOW_HEIGTH)
screen = screen.screen

canvas = Canvas(screen, width=WINDOW_WIDTH,height=WINDOW_HEIGTH)
canvas.pack()

#create area
bounds_x = [100, 620]
bounds_y = [25, 620]

corners = [[100,25],[620,25],[620,620],[100,620]]

canvas.create_line(100,25,620,25,620,620,100,620,100,25)

people = []
delimiter_x = 15
delimiter_y = 15

number_X = 102
number_Y = 84


N_PEOPLE = 30
#spawn people in area
for i in range(0,N_PEOPLE):
    # start_x = numpy.random.randint(100,618)
    # start_y = numpy.random.randint(25,618)
    # if(start_x+delimiter_x >= 618):
    #     start_x = start_x - delimiter_x
    # if(start_y+delimiter_y >= 618):
    #     start_y = start_y - delimiter_y

    start_x = number_X
    start_y = number_Y

    ball = canvas.create_oval(start_x, start_y,start_x+delimiter_x, start_y+delimiter_y, outline="black",
                fill="snow", width=2)
    people.append(ball)
        
    number_X = number_X + 100
    number_Y = number_Y + 119
    if(number_X > 620):
        number_X = 102
    if(number_Y > 620):
        number_Y = 84
    
#get ppl coords for debugging
for p in people:
    print('ID:{},coordinates: {}'.format(p,canvas.coords(p)))

#choose random infected
infected_id = numpy.random.randint(people[0],people[len(people)-1])
print(infected_id)
canvas.itemconfig(infected_id,fill="red")

#for getting mouse position
def motion(event):
    x, y = event.x, event.y
    position.configure(text='{},{}'.format(x,y))

position = Label(screen,text = '0,0')
canvas.create_window(60,20,window = position)

screen.bind('<Motion>', motion)

#random speed for each ball(person)
xspeed,yspeed = [0,0],[0,0]
for _ in range(len(people)):
    move_x,move_y = 0,0
    while(move_x == 0 and move_y == 0):
        move_x = numpy.random.randint(-10,10)
        move_y = numpy.random.randint(-10,10)
    xspeed.append(move_x)
    yspeed.append(move_y)

loop = False
#moving loop
while 1:
    if(loop):
        for p in people:
            x1,y1,x2,y2 = canvas.coords(p)
            x1=int(x1)
            x2=int(x2)
            y1=int(y1)
            y2=int(y2)
            #1st ball middle coords
            middle_x = x1 + (delimiter_x/2)
            middle_y = y1 + (delimiter_y/2)

            for n in people:
                if(n != p):
                    nx1,ny1,nx2,ny2 = canvas.coords(n)
                    nx1=int(nx1)
                    nx2=int(nx2)
                    ny1=int(ny1)
                    ny2=int(ny2)
                    #2nd ball middle coords
                    middle_nx = nx1 + (delimiter_x/2)
                    middle_ny = ny1 + (delimiter_y/2)

                    centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))

                    if(centers_distance <= delimiter_x):
                        print('tukli sa')
                        distance_x = abs(middle_nx-middle_x)
                        distance_y = abs(middle_x-middle_y)
                        if (distance_x <= distance_y):
                            if(canvas.itemcget(n, "fill") == "red" or canvas.itemcget(p,"fill") == "red"):
                                canvas.itemconfig(n,fill="red")
                                canvas.itemconfig(p,fill="red")
                            if ((yspeed[p] > 0 and y1 < ny1) or (yspeed[p] < 0 and y1 > ny1)):
                                yspeed[p] = -yspeed[p]


                            if ((yspeed[n] > 0 and ny1 < y1) or (yspeed[n] < 0 and ny1 > y1)):
                                yspeed[n] = -yspeed[n]



                        elif (distance_x > distance_y):
                            if ((xspeed[p] > 0 and x1 < nx1) or (xspeed[p] < 0 and x1 > nx1)):
                                xspeed[p] = -xspeed[p]

                            if ((xspeed[n] > 0 and nx1 < x1) or (xspeed[n] < 0 and nx1 > x1)):
                                xspeed[n] = -xspeed[n]

                    # if(abs(middle_x - middle_nx) <= delimiter_x and abs(middle_y - middle_ny) <= delimiter_y):
                    #     if(canvas.itemcget(n, "fill") == "red" or canvas.itemcget(p,"fill") == "red"):
                    #         canvas.itemconfig(n,fill="red")
                    #         canvas.itemconfig(p,fill="red")
                        
                    #     xspeed[n] *= -1
                    #     xspeed[p] *= -1
                    #     yspeed[n] *= -1
                    #     yspeed[p] *= -1


            
            # print('x1:{},x2:{},y1:{},y2:{}'.format(x1,x2,y1,y2))
            #1st move to borded then reverse the xspeed and yspeed and move again from the border
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


    #start/pause Q 
    if keyboard.is_pressed('q'):
        if(loop == True):
            loop = False
        else:
            loop = True
    #END program
    if keyboard.is_pressed('e'):
        break
    
    time.sleep(0.05)
    screen.update()
