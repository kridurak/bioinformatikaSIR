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
from Human import *

social_distancing = True
intersecting_aoe = False
intersecting = False
xs = []
ys = []

xsus = []
xrec = []

n_people = 50
probability = 0

num_infected = 0
num_sus = 0
num_recovered = 0

bounds_x_main = [25, 620]
bounds_y_main = [25, 620]

bounds_x_quar = [625, 950]
bounds_y_quar = [250, 620]

people = []
diameter = 10

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
right_frame.pack(side=RIGHT)

canvas = Canvas(left_frame, width=1000,height=WINDOW_HEIGTH)
canvas.pack( side = LEFT)

canvas.create_line(25,25,620,25,620,620,25,620,25,25)

canvas.create_line(313,313,332,313,332,332,313,332,313,313)

canvas.create_line(625,250,950,250,950,620,625,620,625,250)

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
    recovered = 0
    for p in people:
        if(p.color == "green"):
            recovered += 1
    return recovered

#ak sa gulicka stretne s vonkajsou hranou oblasti v strede
def border_of_area_intersect(p,bounds_x_main,bounds_y_main,canvas):
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
        if(middle_x < bounds_x_main[0]):
            testX = bounds_x_main[0]
        elif(middle_x > bounds_x_main[1]):
            testX = bounds_x_main[1]
        if(middle_y < bounds_y_main[0]):
            testY = bounds_y_main[0]
        elif(middle_y > bounds_y_main[1]):
            testY = bounds_y_main[1]

        distance_x = middle_x - testX
        distance_y = middle_y - testY
        distance = sqrt((distance_x*distance_x)+(distance_y*distance_y))

        if(distance <= diameter/2):
            if(testX == bounds_x_main[0]):
                canvas.move(p.id_,bounds_x_main[0]-x2,p.yspeed)
                p.xspeed *= -1
            elif(testX == bounds_x_main[1]):
                canvas.move(p.id_,bounds_x_main[1]-x1,p.yspeed)
                p.xspeed *= -1

            if(testY == bounds_y_main[0]):
                canvas.move(p.id_,p.xspeed,bounds_y_main[0]-y2)
                p.yspeed *= -1
            elif(testY == bounds_y_main[1]):
                canvas.move(p.id_,p.xspeed,bounds_y_main[1]-y1)
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
            
            human = Human(diameter,start_x+diameter/2,start_y+diameter/2,0,ball,start_x,start_y,"blue",True,0,start_x,start_y)
           
            move_x,move_y = 0,0
            while(move_x == 0 and move_y == 0):
                move_x = numpy.random.randint(-10,10)
                move_y = numpy.random.randint(-10,10)
            human.xspeed = move_x
            human.yspeed = move_y
            people.append(human)
# testovanie vsetkych ludi okrem karanteny
def test_everyone():
    for p in people:
        if(p.color == "red" and p.in_quarantine == False):
            p.prob_to_quar = 1
            p.prob_from_quar = 0
            p.move_to_quarantine(canvas)
#testovanie ludi v karantene
def test_people_in_quarantine():
    for p in people:
        if(p.in_quarantine == True and p.color != "red"):
            p.prob_from_quar = 1
            p.move_from_quarantine(canvas)
# spocitanie ludi v karantene
def number_of_people_in_quarantine():
    number = 0
    for p in people:
        if(p.in_quarantine == True):
            number += 1
    return number

spawn_people(n=n_people,diameter=diameter)
print(len(people))
for p in people:
    print('id',p.id_,'speed:',p.xspeed,',',p.yspeed)

########## MENU ########## 

# WIDGET_SLIDER
widget_slider = Scale(canvas,from_= 0, to = 50, orient=HORIZONTAL)
widget_slider.set(15)
widget_slider.pack()
canvas.create_window(200, 670, window=widget_slider)

area_slider = widget_slider.get()

widget_slider2 = Scale(canvas, from_= 0, to = 100, orient=HORIZONTAL)
widget_slider2.set(20)
widget_slider2.pack()
canvas.create_window(445, 670, window=widget_slider2)

widget_slider3 = Scale(canvas, from_= 0, to = 20, orient=HORIZONTAL)
widget_slider3.set(5)
widget_slider3.pack()
canvas.create_window(680, 670, window=widget_slider3)

slider3_value = widget_slider3.get()

# WIDGET_LABELS
widget_label = Label(canvas, text='Number of people in central area: 0')
widget_label.pack()
canvas.create_window(125, 640, window=widget_label)  

widget_label2 = Label(canvas, text='Infection area of effect:')
widget_label2.pack()
canvas.create_window(92, 677, window=widget_label2)

widget_label3 = Label(canvas, text='Probability of infection:')
widget_label3.pack()
canvas.create_window(335, 677, window=widget_label3)

widget_label4 = Label(canvas, text='Number of people in quarantine: 0')
widget_label4.pack()
canvas.create_window(600, 640, window=widget_label4)

widget_label5 = Label(canvas, text='Probability of infection (%): 0')
widget_label5.pack()
canvas.create_window(350, 640, window=widget_label5)

widget_label6 = Label(canvas, text='Social distancing size:')
widget_label6.pack()
canvas.create_window(566, 677, window=widget_label6)

# CHECK_BUTTONS
chcek_button1_status = IntVar()
check_button1 = Checkbutton(canvas, text='Soc. dist.', variable=chcek_button1_status)
check_button1.pack()
canvas.create_window(750, 640, window=check_button1)

check_btn1 = chcek_button1_status.get()

testing_button = Button(canvas,text = "Testing", command = test_everyone)
canvas.create_window(850,640,window = testing_button)

quarantine_button = Button(canvas,text = "Quarantine", command = test_people_in_quarantine)
canvas.create_window(950,640,window = quarantine_button)

# check_button2_status = IntVar()
# check_button2 = Checkbutton(canvas, text='Testing', variable=check_button2_status)
# check_button2.pack()
# canvas.create_window(850, 640, window=check_button2)

# check_btn2 = check_button2_status.get()

# check_button3_status = IntVar()
# check_button3 = Checkbutton(canvas, text='Quarantine', variable=check_button3_status)
# check_button3.pack()
# canvas.create_window(950, 640, window=check_button3)

# check_btn3 = check_button3_status.get()

####### END OF MENU ###### 

while 1:
    if(loop):
        social_distancing = chcek_button1_status.get()
        area_slider = widget_slider.get()
        probability_slider = widget_slider2.get()
        if(probability != probability_slider):
            for p in people:
                p.prob_of_infection = probability_slider
                probability = probability_slider
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
            if(people[rand_number].in_quarantine == False):
                people[rand_number].motion = False
                x,y,_,_ = canvas.coords(people[rand_number].id_)
                people[rand_number].last_x = x
                people[rand_number].last_y = y
                ID = people[rand_number].id_
                canvas.coords(ID,315,315,315+diameter,315+diameter)

        n_people_in_area = 0
        for p in people:
            if(p.color == "red"):
                p.prob_to_quar = 0.01
                p.prob_from_quar = 0
                p.move_to_quarantine(canvas)
            else:
                p.prob_to_quar = 0
                p.prob_from_quar = 0.1
                p.move_from_quarantine(canvas)
            if(p.in_quarantine):
                bounds_x = bounds_x_quar
                bounds_y = bounds_y_quar
            else:
                bounds_x = bounds_x_main
                bounds_y = bounds_y_main

            if(not p.motion):
                n_people_in_area += 1
            canvas.itemconfig(p.id_,fill=p.color)
            if(canvas.itemcget(p.id_, "fill") == "red"):
                p.setOneMoreDay()
                p.recover(200)

            if(p.motion == True):
                p.border_intersect(bounds_x,bounds_y,canvas)
                p.move_self(canvas)
                #border_of_area_intersect(p,[300,345],[300,345],canvas)
            else:
                p.oneMoreDayNoMotion()

            if(p.days_no_motion > 20):
                p.motion = True
                last_x, last_y = p.getLastPosition()
                ID = p.id_
                canvas.coords(ID,last_x,last_y,last_x+diameter,last_y+diameter)
                p.days_no_motion = 0
                p.border_intersect(bounds_x,bounds_y,canvas)
                p.move_self(canvas)
                #border_of_area_intersect(p,[300,345],[300,345],canvas)
            for n in people:
                if(p.in_quarantine == False and n.in_quarantine == False):
                    if(social_distancing):
                        distance_slider = widget_slider3.get()
                        intersecting_aoe = p.social_distancing(area_slider,n,canvas,distance_slider)
                    else:
                        intersecting = p.people_intersect(n,canvas)
                    if(intersecting or intersecting_aoe):
                        if(intersecting):
                            p.prob_of_infection = 100
                        else:
                            p.prob_of_infection = probability_slider
                        if(n.color =="red" or p.color == "red"):
                            if(not (n.color == "green" or p.color == "green")):
                                random_number = numpy.random.randint(0,100)
                                if(p.motion == False):
                                    p.prob_of_infection += 20
                                if(random_number <= p.prob_of_infection):
                                    p.color = "red"
                                    n.color = "red"
        widget_label.configure(text='Number of people in central area: {}'.format(n_people_in_area))
        widget_label5.configure(text='Probability of infection (%): {}'.format(probability_slider)) 
        widget_label4.configure(text='Number of people in quarantine: {}'.format(number_of_people_in_quarantine())) 
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