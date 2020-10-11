from window import Screen
from settings import *
from tkinter import *
import tkinter as tk
from math import *
import numpy, keyboard, time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class human(object):
    def __init__(self,color,x,y,day_of_infection):
        self.color = color
        self.x = x
        self.y = y
        self.day_of_infection = day_of_infection

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

    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color
    
    def setPosition(self,x,y):
        self.x = x
        self.y = y

    def getDay(self):
        return self.day_of_infection
    
    def setOneMoreDay(self):
        self.day_of_infection += 1
    
    def setDay(self,Days):
        self.day_of_infection = Days

# screen = Screen(WINDOW_WIDTH,WINDOW_HEIGTH)
# screen = screen.screen

root = Tk()

left_frame = Frame(root)
left_frame.pack(side=LEFT)

right_frame = Frame(root)
right_frame.pack(side=LEFT)

canvas = Canvas(left_frame, width=700,height=700)
canvas.pack( side = LEFT)
# canvas2 = Canvas(right_frame, width=700,height=700)
# canvas2.pack( side = LEFT)

bounds_x = [100, 620]
bounds_y = [25, 620]

corners = [[100,25],[620,25],[620,620],[100,620]]

canvas.create_line(100,25,620,25,620,620,100,620,100,25)

fig = plt.Figure(figsize=(3,3), dpi=100)
ax = fig.add_subplot(111)
ax.set_title('Graph of increase of number infected people')
ax.set_ylabel('Number infected people')
ax.set_xlim(0,300)
ax.set_ylim(0,35)
graph = FigureCanvasTkAgg(fig,master=right_frame)
graph.get_tk_widget().pack(side="top",fill='both',expand=False)

fig2 = plt.Figure(figsize=(3,3), dpi=100)
ax2 = fig2.add_subplot(111)
ax2.set_title('Susceptible people')
ax2.set_xlim(0,300)
ax2.set_ylim(0,35)
graph2 = FigureCanvasTkAgg(fig2,master=right_frame)
graph2.get_tk_widget().pack(side="left",fill='both',expand=True)

fig3 = plt.Figure(figsize=(3,3), dpi=100)
ax3 = fig3.add_subplot(111)
ax3.set_title('Recovered people')
ax3.set_xlim(0,300)
ax3.set_ylim(0,35)
graph3 = FigureCanvasTkAgg(fig3,master=right_frame)
graph3.get_tk_widget().pack(side="bottom",fill='both',expand=True)

xs = []
ys = []

xsus = []

people = []
diameter_x = 15
diameter_y = 15

number_X = 102
number_Y = 84

def animate(infected, timer, susceptible):
    # Add x and y to lists
    xs.append(infected)
    ys.append(timer)
    xsus.append(susceptible)

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.set_title('Graph of increase of number infected people')
    ax.set_xlim(0,300)
    ax.set_ylim(0,35)
    ax.plot(ys, xs)
    
    ax2.clear()
    ax2.set_title('Susceptible people')
    ax2.set_xlim(0,300)
    ax2.set_ylim(-5,35)
    ax2.plot(ys, xsus)
    
    ax3.clear()
    ax3.set_title('Recovered people')
    ax3.set_xlim(0,300)
    ax3.set_ylim(0,35)
    ax3.plot(ys, xs)

    # Format plot
    # animation.FuncAnimation(fig, animate, fargs=(xs, ys),interval = 0)
    graph.draw()
    # animation.FuncAnimation(fig2, animate, fargs=(xs, ys),interval = 0)
    graph2.draw()
    # animation.FuncAnimation(fig3, animate, fargs=(xs, ys),interval = 0)
    graph3.draw()

def number_of_infected():
    infected = 0
    for p in people:
        if(canvas.itemcget(p, "fill") == "red"):
            infected += 1
    susceptible = len(people) - infected
    return infected, susceptible

for i in range(0,30):
    # start_x = numpy.random.randint(100,618)
    # start_y = numpy.random.randint(25,618)
    # if(start_x+delimiter_x >= 618):
    #     start_x = start_x - delimiter_x
    # if(start_y+delimiter_y >= 618):
    #     start_y = start_y - delimiter_y

    start_x = number_X
    start_y = number_Y

    ball = canvas.create_oval(start_x, start_y,start_x+diameter_x, start_y+diameter_y, outline="black",
                fill="snow", width=2)
    people.append(ball)

    number_X = number_X + 100
    number_Y = number_Y + 119
    if(number_X > 620):
        number_X = 102
    if(number_Y > 620):
        number_Y = 84

# for p in people:
#     print('ID:{},coordinates: {}'.format(p,canvas.coords(p)))


infected_id = numpy.random.randint(people[0],people[len(people)-1])
# print(infected_id)
canvas.itemconfig(infected_id,fill="red")

# def motion(event):
#     x, y = event.x, event.y
#     position.configure(text='{},{}'.format(x,y))

# position = Label(screen,text = '0,0')
# canvas.create_window(60,20,window = position)

# screen.bind('<Motion>', motion)

loop = False
xspeed,yspeed = [0,0],[0,0]
for _ in range(len(people)):
    move_x,move_y = 0,0
    while(move_x == 0 and move_y == 0):
        move_x = numpy.random.randint(-10,10)
        move_y = numpy.random.randint(-10,10)
    xspeed.append(move_x)
    yspeed.append(move_y)

timer = 0

while 1:
    if(loop):
        timer += 1
        for p in people:
            x1,y1,x2,y2 = canvas.coords(p)
            x1=int(x1)
            x2=int(x2)
            y1=int(y1)
            y2=int(y2)
            #1st ball middle coords
            middle_x = x1 + (diameter_x/2)
            middle_y = y1 + (diameter_y/2)

            for n in people:
                if(n != p):
                    nx1,ny1,nx2,ny2 = canvas.coords(n)
                    nx1=int(nx1)
                    nx2=int(nx2)
                    ny1=int(ny1)
                    ny2=int(ny2)
                    #2nd ball middle coords
                    middle_nx = nx1 + (diameter_x/2)
                    middle_ny = ny1 + (diameter_y/2)

                    centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))

                    if(centers_distance <= diameter_x):
                        # print('tukli sa')
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

                    # if(abs(middle_x - middle_nx) <= diameter_x and abs(middle_y - middle_ny) <= diameter_y):
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
        number_people = number_of_infected()
        number_infected = number_people[0]
        number_susceptible = number_people[1]
        # print("infected: ",number_infected,", time:", timer)
        if(timer % 2 == 0):
            animate(number_infected,timer,number_susceptible)


    if keyboard.is_pressed('q'):
        if(loop == True):
            loop = False
        else:
            loop = True
    if keyboard.is_pressed('e'):
        break

    time.sleep(0)
    root.update()

    # screen.update()