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

xs = []
ys = []

xsus = []
xrec = []

n_people = 30

num_infected = 0
num_sus = 0
num_recovered = 0

bounds_x = [25, 620]
bounds_y = [25, 620]

corners = [[25,25],[620,25],[620,620],[25,620]]

people = []
diameter_x = 15
diameter_y = 15

number_X = 102
number_Y = 84

timer = 0
loop = False
xspeed,yspeed = [0,0],[0,0]
infected_id=0
class Human(object):
    def __init__(self,start_x,start_y,day_of_infection,id_, x , y,color):
        self.color = color
        self.id_ = id_
        self.start_x = start_x
        self.start_y = start_y
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
    
    def recover(self, days):
        if(self.day_of_infection >= days):
            self.color = "green"

screen = Screen(WINDOW_WIDTH,WINDOW_HEIGTH)
screen = screen.screen

left_frame = Frame(screen)
left_frame.pack(side=LEFT)

right_frame = Frame(screen)
right_frame.pack(side=LEFT)

canvas = Canvas(left_frame, width=700,height=700)
canvas.pack( side = LEFT)


canvas.create_line(25,25,620,25,620,620,25,620,25,25)

fig = plt.Figure(figsize=(8,5), dpi=100)
ax = fig.add_subplot(111)
ax.set_title('SIR model')
ax.set_xlim(0,1)
ax.set_ylim(0,n_people+5)

ax.plot(ys, xs, label='N_Infected', color = 'red')
ax.plot(ys,xsus, label='N_Susceptible', color = 'blue')
ax.plot(ys,xrec, label='N_Recovered', color = 'green')

ax.legend()
graph = FigureCanvasTkAgg(fig,master=right_frame)
graph.get_tk_widget().pack(side="top",fill='both',expand=False)


def animate(infected, timer, susceptible,recovered, n_people):
    # Add x and y to lists
    xs.append(infected)
    ys.append(timer)
    xsus.append(susceptible)
    xrec.append(recovered)

    # Draw x and y lists
    ax.clear()
    ax.set_title('SIR model')
    ax.set_xlim(0,timer)
    ax.set_ylim(0,n_people+5)
    
    ax.plot(ys, xs, label='N_Infected', color = 'red')
    ax.plot(ys,xsus, label='N_Susceptible', color = 'blue')
    ax.plot(ys,xrec, label='N_Recovered', color = 'green')

    ax.legend()
    
    graph.draw()

def number_of_infected(people):
    infected = 0
    for p in people:
        if(p.color == "red"):
            infected += 1
    return infected

def number_of_recovered(people):
    infected = 0
    for p in people:
        if(p.color == "green"):
            infected += 1
    return infected

def social_distancing(R,p,xspeed,yspeed,canvas):
    bounds_x = [p.start_x-R,p.start_x+R]
    bounds_y = [p.start_y-R,p.start_y+R]
    p = p.id_
    x1,y1,x2,y2 = canvas.coords(p)
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    #1st ball middle coords
    middle_x = x1 + (diameter_x/2)
    middle_y = y1 + (diameter_y/2)
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

def people_intersect(p,n,canvas):
    intersecting = False
    x1,y1,x2,y2 = canvas.coords(p)
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    #1st ball middle coords
    middle_x = x1 + (diameter_x/2)
    middle_y = y1 + (diameter_y/2)

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
                intersecting = True
                    

                if ((yspeed[p] > 0 and y1 < ny1) or (yspeed[p] < 0 and y1 > ny1)):
                    yspeed[p] = -yspeed[p]


                if ((yspeed[n] > 0 and ny1 < y1) or (yspeed[n] < 0 and ny1 > y1)):
                    yspeed[n] = -yspeed[n]



            elif (distance_x > distance_y):
                if ((xspeed[p] > 0 and x1 < nx1) or (xspeed[p] < 0 and x1 > nx1)):
                    xspeed[p] = -xspeed[p]

                if ((xspeed[n] > 0 and nx1 < x1) or (xspeed[n] < 0 and nx1 > x1)):
                    xspeed[n] = -xspeed[n]
    return intersecting

def border_intersect(p,bounds_x,bounds_y,xspeed,yspeed,canvas):
    x1,y1,x2,y2 = canvas.coords(p)
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    #1st ball middle coords
    middle_x = x1 + (diameter_x/2)
    middle_y = y1 + (diameter_y/2)
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



for i in range(0,n_people):
    # start_x = numpy.random.randint(100,618)
    # start_y = numpy.random.randint(25,618)
    # if(start_x+delimiter_x >= 618):
    #     start_x = start_x - delimiter_x
    # if(start_y+delimiter_y >= 618):
    #     start_y = start_y - delimiter_y

    start_x = number_X
    start_y = number_Y

    
    ball = canvas.create_oval(start_x, start_y,start_x+diameter_x, start_y+diameter_y, outline="black",
                fill="blue", width=2)
    
    human = Human(start_x+diameter_x/2,start_y+diameter_y/2,0,ball,start_x,start_y,"blue")
    people.append(human)

    number_X = number_X + 100
    number_Y = number_Y + 119
    if(number_X > 620):
        number_X = 102
    if(number_Y > 620):
        number_Y = 84

# for p in people:
#     print('ID:{},coordinates: {}'.format(p,canvas.coords(p)))


# infected_id = numpy.random.randint(people[0],people[len(people)-1])
# # print(infected_id)
# num_infected += 1
# canvas.itemconfig(infected_id,fill="red")

# def motion(event):
#     x, y = event.x, event.y
#     position.configure(text='{},{}'.format(x,y))

# position = Label(screen,text = '0,0')
# canvas.create_window(60,20,window = position)

# screen.bind('<Motion>', motion)

w2 = Scale(screen, from_=15, to=595, orient=HORIZONTAL)
w2.set(15)
w2.pack()

slider_value = w2.get()

canvas.create_window(60,650,window=w2)

for _ in range(len(people)):
    move_x,move_y = 0,0
    while(move_x == 0 and move_y == 0):
        move_x = numpy.random.randint(-10,10)
        move_y = numpy.random.randint(-10,10)
    xspeed.append(move_x)
    yspeed.append(move_y)

while 1:
    if(loop):
        slider_value = w2.get()
        timer += 1
        if(timer == 10):
            infected_id = numpy.random.randint(people[0].id_,people[len(people)-1].id_)
            num_infected += 1
            for p in people:
                if(p.id_ == infected_id):
                    p.color = "red"
            
        for p in people:
            canvas.itemconfig(p.id_,fill=p.color)
            if(canvas.itemcget(p.id_, "fill") == "red"):
                p.setOneMoreDay()
                p.recover(200)
            social_distancing(slider_value,p,xspeed,yspeed,canvas)
            border_intersect(p.id_,bounds_x,bounds_y,xspeed,yspeed,canvas)
            for n in people:
                intersecting = people_intersect(p.id_,n.id_,canvas)
                if(intersecting):
                    if(n.color =="red" or p.color == "red"):
                        if(not n.color == "green" or p.color == "green"):
                            p.color = "red"
                            n.color = "red"
                        # canvas.itemconfig(n,fill="red")
                        # canvas.itemconfig(p,fill="red")
            
            
        num_infected = number_of_infected(people)
        num_recovered = number_of_recovered(people)
        num_sus = len(people) - num_infected - num_recovered
        #print("infected: ",num_infected,", time:", timer)
        if(timer % 2 == 0):
            animate(num_infected,timer,num_sus,num_recovered,n_people)


    if keyboard.is_pressed('q'):
        if(loop == True):
            loop = False
        else:
            loop = True
    if keyboard.is_pressed('e'):
        break

    time.sleep(0)
    screen.update()

    # screen.update()