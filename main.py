from window import Screen
from settings import *
from tkinter import *
import tkinter as tk
from math import *
import random
import numpy, keyboard, time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Human import *

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
diameter = 15

number_X = 102
number_Y = 84

timer = 0
loop = False
infected_id=0

screen = Screen(WINDOW_WIDTH,WINDOW_HEIGTH)
screen = screen.screen

left_frame = Frame(screen)
left_frame.pack(side=LEFT)

right_frame = Frame(screen)
right_frame.pack(side=LEFT)

canvas = Canvas(left_frame, width=700,height=700)
canvas.pack( side = LEFT)


canvas.create_line(25,25,620,25,620,620,25,620,25,25)

canvas.create_line(313,313,332,313,332,332,313,332,313,313)

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

#graf
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
#pocet nakazenych
def number_of_infected(people):
    infected = 0
    for p in people:
        if(p.color == "red"):
            infected += 1
    return infected
#pocet vyliecenych
def number_of_recovered(people):
    infected = 0
    for p in people:
        if(p.color == "green"):
            infected += 1
    return infected

def social_distancing(R,p,n,canvas):
    if(p.motion and n.motion):
        intersecting = False
        x1,y1,x2,y2 = canvas.coords(p.id_)
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)
        #1st ball middle coords
        middle_x = x1 + (diameter/2)
        middle_y = y1 + (diameter/2)
        if(n != p):
            nx1,ny1,nx2,ny2 = canvas.coords(n.id_)
            nx1=int(nx1)
            nx2=int(nx2)
            ny1=int(ny1)
            ny2=int(ny2)
            #2nd ball middle coords
            middle_nx = nx1 + (diameter/2)
            middle_ny = ny1 + (diameter/2)

            centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))
            if(centers_distance <= 25):
                distance_x = abs(middle_nx-middle_x)
                distance_y = abs(middle_x-middle_y)
                if(distance_x > distance_y):
                    if(middle_y > middle_ny):
                        canvas.move(p.id_,0,25-distance_y)
                    else:
                        canvas.move(p.id_,0,(25-distance_y)*-1)
                else:
                    if(middle_x > middle_nx):
                        canvas.move(p.id_,25-distance_x,0)
                    else:
                        canvas.move(p.id_,(25-distance_x)*-1,0)

            if(centers_distance <= diameter+R):
                intersecting = True
            return intersecting

#ak sa stretnu 2 gulicky
def people_intersect(p,n,canvas):
    if(p.motion and n.motion):
        intersecting = False
        x1,y1,x2,y2 = canvas.coords(p.id_)
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)
        #1st ball middle coords
        middle_x = x1 + (diameter/2)
        middle_y = y1 + (diameter/2)

        if(n != p):
            nx1,ny1,nx2,ny2 = canvas.coords(n.id_)
            nx1=int(nx1)
            nx2=int(nx2)
            ny1=int(ny1)
            ny2=int(ny2)
            #2nd ball middle coords
            middle_nx = nx1 + (diameter/2)
            middle_ny = ny1 + (diameter/2)

            centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))

            if(centers_distance <= diameter):
                # print('tukli sa')
                distance_x = abs(middle_nx-middle_x)
                distance_y = abs(middle_x-middle_y)
                if (distance_x <= distance_y):
                    intersecting = True
                        

                    if ((p.yspeed > 0 and y1 < ny1) or (p.yspeed < 0 and y1 > ny1)):
                        p.yspeed = -p.yspeed


                    if ((n.yspeed > 0 and ny1 < y1) or (n.yspeed < 0 and ny1 > y1)):
                        n.yspeed = -n.yspeed



                elif (distance_x > distance_y):
                    if ((p.xspeed > 0 and x1 < nx1) or (p.xspeed < 0 and x1 > nx1)):
                        p.xspeed = -p.xspeed

                    if ((n.xspeed > 0 and nx1 < x1) or (n.xspeed < 0 and nx1 > x1)):
                        n.xspeed = -n.xspeed
        return intersecting
#ak sa gulicka stretne s vonkajsou hranou oblasti
def border_intersect(p,bounds_x,bounds_y,canvas):
    x1,y1,x2,y2 = canvas.coords(p.id_)
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    #1st move to borded then reverse the xspeed and yspeed and move again from the border
    if(x1+p.xspeed < bounds_x[0]):
        if(y1+p.yspeed < bounds_y[0]):
            canvas.move(p.id_,bounds_x[0]-x1,bounds_y[0]-y1)
            p.yspeed *= -1
        elif(y2+p.yspeed> bounds_y[1]):
            canvas.move(p.id_,bounds_x[0]-x1,bounds_y[1]-y2)
            p.yspeed *= -1
        else:    
            canvas.move(p.id_,bounds_x[0]-x1,p.yspeed)
        p.xspeed *= -1
        #canvas.move(infected_id,move_x,move_y)
    elif(x2+p.xspeed > bounds_x[1]):
        if(y1+p.yspeed < bounds_y[0]):
            canvas.move(p,bounds_x[1]-x2,bounds_y[0]-y1)
            p.yspeed *= -1
        elif(y2+p.yspeed > bounds_y[1]):
            canvas.move(p.id_,bounds_x[1]-x2,bounds_y[1]-y2)
            p.yspeed *= -1
        else:    
            canvas.move(p.id_,bounds_x[1]-x2,p.yspeed)
        p.xspeed *= -1
    else:
        if(y1+p.yspeed < bounds_y[0]):
            canvas.move(p.id_,p.xspeed,bounds_y[0]-y1)
            p.yspeed *= -1
        elif(y2+p.yspeed > bounds_y[1]):
            canvas.move(p.id_,p.xspeed,bounds_y[1]-y2)
            p.yspeed *= -1
        else:    
            canvas.move(p.id_,p.xspeed,p.yspeed)
#ak sa gulicka stretne s vonkajsou hranou oblasti v strede
def border_of_area_intersect(p,bounds_x,bounds_y,canvas):
    if(p.motion == True):
        x1,y1,x2,y2 = canvas.coords(p.id_)
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)
        #1st move to borded then reverse the xspeed and yspeed and move again from the border

        middle_x = x1+diameter/2
        middle_y = y1+diameter/2

        testX = middle_x
        testY = middle_y
        if(middle_x < bounds_x[0]):
            testX = bounds_x[0]
        elif(middle_x > bounds_x[1]):
            testX = bounds_x[1]
        if(middle_y < bounds_y[0]):
            testY = bounds_y[0]
        elif(middle_y > bounds_y[1]):
            testY = bounds_y[1]

        distance_x = middle_x - testX
        distance_y = middle_y - testY
        distance = sqrt((distance_x*distance_x)+(distance_y*distance_y))

        if(distance <= diameter/2):
            if(testX == bounds_x[0]):
                canvas.move(p.id_,bounds_x[0]-x2,p.yspeed)
                p.xspeed *= -1
            elif(testX == bounds_x[1]):
                canvas.move(p.id_,bounds_x[1]-x1,p.yspeed)
                p.xspeed *= -1

            if(testY == bounds_y[0]):
                canvas.move(p.id_,p.xspeed,bounds_y[0]-y2)
                p.yspeed *= -1
            elif(testY == bounds_y[1]):
                canvas.move(p.id_,p.xspeed,bounds_y[1]-y1)
                p.yspeed *= -1
#pridaj ludi na canvas
def spawn_people(n,diameter):
    forbidden_spawn_coords = [[300,300,345,345]]
    for i in range(0,n):        
        passed = False
        while(not passed):
            start_x = numpy.random.randint(100,618)
            start_y = numpy.random.randint(25,618)
            if(start_x+diameter >= 618):
                start_x = start_x - diameter
            if(start_y+diameter >= 618):
                start_y = start_y - diameter
            for coords in forbidden_spawn_coords:
                if(start_x+diameter < coords[0] or start_y+diameter < coords[1] \
                        or start_x > coords[2] or start_y > coords[3]):
                        passed = True
                else:
                    passed = False
                    break

        if(passed):
            forbidden_spawn_coords.append([start_x,start_y,start_x+diameter,start_y+diameter])

            ball = canvas.create_oval(start_x, start_y,start_x+diameter, start_y+diameter, outline="black",
                        fill="blue", width=2)
            
            human = Human(start_x+diameter/2,start_y+diameter/2,0,ball,start_x,start_y,"blue",True,0,start_x,start_y)
           
            move_x,move_y = 0,0
            while(move_x == 0 and move_y == 0):
                move_x = numpy.random.randint(-10,10)
                move_y = numpy.random.randint(-10,10)
            human.xspeed = move_x
            human.yspeed = move_y
            people.append(human)

spawn_people(n=n_people,diameter=diameter)
print(len(people))
for p in people:
    print('id',p.id_,'speed:',p.xspeed,',',p.yspeed)

widget_label = Label(canvas, text='Number of people in central area: 0')
widget_label.pack()
canvas.create_window(125, 640, window=widget_label)  

widget_label2 = Label(canvas, text='Infection area of effect:')
widget_label2.pack()
canvas.create_window(125, 675, window=widget_label2) 

widget_slider = Scale(canvas,from_= 0, to = 50, orient=HORIZONTAL)
widget_slider.set(5)
widget_slider.pack()
canvas.create_window(240, 670, window=widget_slider)

slider_value = widget_slider.get()

while 1:
    if(loop):
        slider_value = widget_slider.get()
        timer += 1
        if(timer == 10):
            infected_id = numpy.random.randint(people[0].id_,people[len(people)-1].id_)
            num_infected += 1
            for p in people:
                if(p.id_ == infected_id):
                    p.color = "red"
            
# choice random human and set middle position
        rand_number = random.randint(0,100)
        if(rand_number < 30):
            people[rand_number].motion = False
            x,y,_,_ = canvas.coords(people[rand_number].id_)
            people[rand_number].last_x = x
            people[rand_number].last_y = y
            ID = people[rand_number].id_
            canvas.coords(ID,315,315,315+diameter,315+diameter)

        n_people_in_area = 0
        for p in people:
            if(not p.motion):
                n_people_in_area += 1
            canvas.itemconfig(p.id_,fill=p.color)
            if(canvas.itemcget(p.id_, "fill") == "red"):
                p.setOneMoreDay()
                p.recover(200)

            if(p.motion == True):
                border_intersect(p,bounds_x,bounds_y,canvas)
                #border_of_area_intersect(p,[300,345],[300,345],canvas)
            else:
                p.oneMoreDayNoMotion()

            if(p.days_no_motion > 20):
                p.motion = True
                last_x, last_y = p.getLastPosition()
                ID = p.id_
                canvas.coords(ID,last_x,last_y,last_x+diameter,last_y+diameter)
                p.days_no_motion = 0
                border_intersect(p,bounds_x,bounds_y,canvas)
                #border_of_area_intersect(p,[300,345],[300,345],canvas)
            for n in people:
                intersecting_aoe = social_distancing(slider_value,p,n,canvas)
                intersecting = people_intersect(p,n,canvas)
                if(intersecting or intersecting_aoe):
                    if(n.color =="red" or p.color == "red"):
                        if(not (n.color == "green" or p.color == "green")):
                            p.color = "red"
                            n.color = "red"
                        # canvas.itemconfig(n,fill="red")
                        # canvas.itemconfig(p,fill="red")
            
        widget_label.configure(text='Number of people in central area: {}'.format(n_people_in_area)) 
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