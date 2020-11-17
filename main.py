from window import Screen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from math import *
import numpy, keyboard, time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Human import *

##############SETTINGS###################
WINDOW_WIDTH = 1550
WINDOW_HEIGTH = 720

#####-------TAB 1--------########
Settings_Tab1 = {'social_distancing' : False,
'quarantine' : False,
'n_people' : 0,
'n_areas' : 0,
'central' : False,
'max_speed' : 10,
'prob_of_infection' : 0,
'size_of_infection_area' : 0,
'rules_sample' : 50,
'mobility' : False
}


bounds_x_dict = { 1:[[20,620]],
                2:[[25,315],[325,615]],
                3:[[20,213],[223.5,416.5],[427,620]],
                4:[[25,315],[325,615],[25,315],[325,615]],
                5:[[20,213],[223.5,416.5],[427,620],[121.75,314.75],[325.25,518.25]],
                6:[[20,213],[223.5,416.5],[427,620],[20,213],[223.5,416.5],[427,620]],
                7:[[20,213],[223.5,416.5],[427,620],[20,213],[223.5,416.5],[427,620],[223.5,416.5]],
                8:[[20,213],[223.5,416.5],[427,620],[20,213],[223.5,416.5],[427,620],[121.75,314.75],[325.25,518.25]],
                9:[[20,213],[223.5,416.5],[427,620],[20,213],[223.5,416.5],[427,620],[20,213],[223.5,416.5],[427,620]]
}

bounds_y_dict = { 1:[[20,620]],
                2:[[170,470],[170,470]],
                3:[[220,420],[220,420],[220,420]],
                4:[[25,315],[25,315],[325,615],[325,615]],
                5:[[114.75,314.75],[114.75,314.75],[114.75,314.75],[325.25,525.25],[325.25,525.25]],
                6:[[114.75,314.75],[114.75,314.75],[114.75,314.75],[325.25,525.25],[325.25,525.25],[325.25,525.25]],
                7:[[20,213],[20,213],[20,213],[223.5,416.5],[223.5,416.5],[223.5,416.5],[427,620]],
                8:[[20,213],[20,213],[20,213],[223.5,416.5],[223.5,416.5],[223.5,416.5],[427,620],[427,620]],
                9:[[20,213],[20,213],[20,213],[223.5,416.5],[223.5,416.5],[223.5,416.5],[427,620],[427,620],[427,620]]
}

bxq = [630, 830]
byq = [420, 620]


social_distancing = True
quarantine = False

n_areas = 0

intersecting_aoe = False
intersecting = False
xs = []
ys = []
xs2 = []
ys2 = []
xs3 = []
ys3 = []

xsus = []
xrec = []

xsus2 = []
xrec2 = []
xsus3 = []
xrec3 = []

n_people = 60
n_people2 = 90
probability = 0

num_infected = 0
num_sus = 0
num_recovered = 0

bounds_x_main = [25, 550]
bounds_y_main = [25, 550]

bounds_x_quar = [560, 800]
bounds_y_quar = [310, 550]

bounds_x_central = [(bounds_x_main[1]-bounds_x_main[0])/2-8+bounds_x_main[0],(bounds_x_main[1]-bounds_x_main[0])/2+8+bounds_x_main[0]]
bounds_y_central = [(bounds_y_main[1]-bounds_y_main[0])/2-8+bounds_y_main[0],(bounds_y_main[1]-bounds_y_main[0])/2+8+bounds_y_main[0]]

people = []
people2 = []
people3 = []
diameter = 10

rules_sample = 0
ppl_without_rules = []


number_X = 102
number_Y = 84

timer_tab1 = 0
timer_tab2 = 0
timer_tab3 = 0

loop = False
infected_id=0

##############################################

#######-----TAB2-----#######
bounds_x_main2 = [[25,275],[287,537],[549,799],[25,275],[287,537],[549,799],[25,275],[287,537],[549,799]]
bounds_y_main2 = [[25,215],[25,215],[25,215],[227,417],[227,417],[227,417],[429,619],[429,619],[429,619]]

bounds_x_quar2 = [805,1000]
bounds_y_quar2 = [429,619]

rules_sample2 = 0
ppl_without_rules2 = []

####################################### SETTINGS ################################################
SCREEN = Screen('settings',500,800)
screen = SCREEN.screen

settings_window = Frame(screen)
settings_window.pack()

def create_world():
    Settings_Tab1['n_people'] = int(TXT_BOX.get())
    Settings_Tab1['social_distancing'] = bool(CHCK_BTN2_STATUS.get())
    Settings_Tab1['quarantine'] = bool(CHCK_BTN1_STATUS.get())
    Settings_Tab1['n_areas'] = int(TXT_BOX2.get())
    Settings_Tab1['central'] = False
    Settings_Tab1['max_speed'] = int(SLIDER_SPEED.get())
    Settings_Tab1['prob_of_infection'] = int(SLIDER_POF.get())
    Settings_Tab1['size_of_infection_area'] = int(SLIDER_AREA.get())
    if(Settings_Tab1['n_areas'] > 1):
        Settings_Tab1['mobility'] = bool(CHCK_BTN3_STATUS.get())
    Settings_Tab1['rules_sample'] = int(SLIDER_SAMPLE.get())
    settings_window.destroy()
    screen.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGTH))
    SCREEN.name = 'main'

settings_canvas = Canvas(settings_window,width=500,height=800)
settings_canvas.pack()

LABEL1 = Label(settings_canvas, text='Number of people(int):')
LABEL1.place(relx = 0, rely = 0)

TXT_BOX = Entry(settings_canvas)
TXT_BOX.place(relx = 0.255, rely = 0.001)

LABEL2 = Label(settings_canvas, text='Number of areas(int 1-9):')
LABEL2.place(relx = 0, rely = 0.05)

TXT_BOX2 = Entry(settings_canvas)
TXT_BOX2.place(relx = 0.275, rely = 0.05)

# CHECK_BUTTONS
CHCK_BTN1_STATUS = IntVar()
CHCK_BTN1 = Checkbutton(settings_canvas, text='Quarantine', variable=CHCK_BTN1_STATUS)
CHCK_BTN1.place(relx = 0, rely = 0.1)

CHCK_BTN2_STATUS = IntVar()
CHCK_BTN2 = Checkbutton(settings_canvas, text='Social distancing', variable=CHCK_BTN2_STATUS)
CHCK_BTN2.place(relx = 0, rely = 0.15)

LABEL3 = Label(settings_canvas, text='Max.speed:')
LABEL3.place(relx = 0, rely = 0.2)

SLIDER_SPEED = Scale(settings_canvas,from_= 1, to = 10, orient=HORIZONTAL)
SLIDER_SPEED.set(10)
SLIDER_SPEED.place(relx = 0, rely = 0.22)

LABEL4 = Label(settings_canvas, text='Probability of infection:')
LABEL4.place(relx = 0, rely = 0.28)

SLIDER_POF = Scale(settings_canvas,from_= 0, to = 100, orient=HORIZONTAL)
SLIDER_POF.set(50)
SLIDER_POF.place(relx = 0, rely = 0.31)

LABEL5 = Label(settings_canvas, text='Infectious area:')
LABEL5.place(relx = 0, rely = 0.38)

SLIDER_AREA = Scale(settings_canvas,from_= 0, to = 50, orient=HORIZONTAL)
SLIDER_AREA.set(20)
SLIDER_AREA.place(relx = 0, rely = 0.41)

CHCK_BTN3_STATUS = IntVar()
CHCK_BTN3 = Checkbutton(settings_canvas, text='Mobility', variable=CHCK_BTN3_STATUS)
CHCK_BTN3.place(relx = 0, rely = 0.48)

LABEL6 = Label(settings_canvas, text='Rules do not apply, size of sample(%):')
LABEL6.place(relx = 0, rely = 0.54)

SLIDER_SAMPLE = Scale(settings_canvas,from_= 0, to = 100, orient=HORIZONTAL)
SLIDER_SAMPLE.set(20)
SLIDER_SAMPLE.place(relx = 0, rely = 0.58)


generate_btn = Button(settings_canvas,text = "GENERATE", command = create_world)
generate_btn.place(relx = 0.45, rely = 0.95)

while(SCREEN.name == 'settings'):
    screen.update()
  
#########################################################################################################
def generate_areas(cnv,n_areas,bx,by,quar,bxq,byq):
    #calculate width and height of one rectangle
    b_x = bx[n_areas]
    b_y = by[n_areas]
    for i in range(len(b_x)):
        bounds_x = b_x[i]
        bounds_y = b_y[i]
        cnv.create_rectangle(bounds_x[0],bounds_y[0],bounds_x[1],bounds_y[1])
    if(quar):
        cnv.create_rectangle(bxq[0],byq[0],bxq[1],byq[1])


if(SCREEN.name != 'settings'):
    notebook = ttk.Notebook(screen)

    tab1 = Frame(notebook)
    tab2 = Frame(notebook)
    tab3 = Frame(notebook)

    notebook.add(tab1, text='Tab 1')
    notebook.add(tab2, text='Tab 2')
    notebook.add(tab3, text='Tab 3')

    notebook.pack(expand = 1, fill="both")
    
    left_frame_tab3 = Frame(tab3,width=900)
    left_frame_tab3.pack(side=LEFT)

    right_frame_tab3 = Frame(tab3)
    right_frame_tab3.pack(side=RIGHT)
    canvas3 = Canvas(left_frame_tab3, width=900,height=WINDOW_HEIGTH)
    canvas3.pack( side = LEFT)

    cnvq = Canvas(right_frame_tab3,width=650,height=200)
    cnvq.pack(side=BOTTOM)

    generate_areas(canvas3,Settings_Tab1['n_areas'],bounds_x_dict,bounds_y_dict,Settings_Tab1['quarantine'],bxq,byq)

    fig3 = plt.Figure(figsize=(8,5), dpi=100)
    ax3 = fig3.add_subplot(111)
    ax3.set_title('SIR model')
    ax3.set_xlim(0,1)
    ax3.set_ylim(0,Settings_Tab1['n_people']+5)

    ax3.plot(ys, xs, label='N_Infected', color = 'red')
    ax3.plot(ys,xsus, label='N_Susceptible', color = 'blue')
    ax3.plot(ys,xrec, label='N_Recovered', color = 'green')

    ax3.legend()
    graph3 = FigureCanvasTkAgg(fig3,master=right_frame_tab3)
    graph3.get_tk_widget().pack(side="top",fill='both',expand=False)
    #cnvq.create_window(0,0,window=graph3)

    left_frame_tab1 = Frame(tab1)
    left_frame_tab1.pack(side=LEFT)

    right_frame_tab1 = Frame(tab1)
    right_frame_tab1.pack(side=RIGHT)

    left_frame_tab2 = Frame(tab2)
    left_frame_tab2.pack(side=LEFT)

    right_frame_tab2 = Frame(tab2)
    right_frame_tab2.pack(side=RIGHT)

    canvas = Canvas(left_frame_tab1, width=1000,height=WINDOW_HEIGTH)
    canvas.pack( side = LEFT)

    canvas2 = Canvas(left_frame_tab2, width = 1000, height = WINDOW_HEIGTH)
    canvas2.pack( side = LEFT)

    for i in range(0,9):
        bounds_x = bounds_x_main2[i]
        bounds_y = bounds_y_main2[i]
        canvas2.create_rectangle(bounds_x[0],bounds_y[0],bounds_x[1],bounds_y[1])

    canvas2.create_rectangle(bounds_x_quar2[0],bounds_y_quar2[0],bounds_x_quar2[1],bounds_y_quar2[1])

    canvas.create_rectangle(bounds_x_main[0],bounds_y_main[0],bounds_x_main[1],bounds_y_main[1])
    canvas.create_rectangle(bounds_x_central[0],bounds_y_central[0],bounds_x_central[1],bounds_y_central[1])
    canvas.create_rectangle(bounds_x_quar[0],bounds_y_quar[0],bounds_x_quar[1],bounds_y_quar[1])

    fig = plt.Figure(figsize=(8,5), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title('SIR model')
    ax.set_xlim(0,1)
    ax.set_ylim(0,n_people+5)

    ax.plot(ys, xs, label='N_Infected', color = 'red')
    ax.plot(ys,xsus, label='N_Susceptible', color = 'blue')
    ax.plot(ys,xrec, label='N_Recovered', color = 'green')

    ax.legend()
    graph = FigureCanvasTkAgg(fig,master=right_frame_tab1)
    graph.get_tk_widget().pack(side="top",fill='both',expand=False)

    fig2 = plt.Figure(figsize=(8,5), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.set_title('SIR model')
    ax2.set_xlim(0,1)
    ax2.set_ylim(0,95)

    ax2.plot(ys2, xs2, label='N_Infected', color = 'red')
    ax2.plot(ys2,xsus2, label='N_Susceptible', color = 'blue')
    ax2.plot(ys2,xrec2, label='N_Recovered', color = 'green')

    ax2.legend()
    graph2 = FigureCanvasTkAgg(fig2,master=right_frame_tab2)
    graph2.get_tk_widget().pack(side="top",fill='both',expand=False)

    #graf
    def animate(infected, timer_tab1, susceptible,recovered, n_people):
        # Add x and y to lists
        xs.append(infected)
        ys.append(timer_tab1)
        xsus.append(susceptible)
        xrec.append(recovered)

        # Draw x and y lists
        ax.clear()
        ax.set_title('SIR model')
        ax.set_xlim(0,timer_tab1)
        ax.set_ylim(0,n_people+5)
        
        ax.plot(ys, xs, label='N_Infected', color = 'red')
        ax.plot(ys,xsus, label='N_Susceptible', color = 'blue')
        ax.plot(ys,xrec, label='N_Recovered', color = 'green')

        ax.legend()
        
        graph.draw()

    def animate2(infected, timer_tab2, susceptible,recovered, n_people):
        # Add x and y to lists
        xs2.append(infected)
        ys2.append(timer_tab2)
        xsus2.append(susceptible)
        xrec2.append(recovered)

        # Draw x and y lists
        ax2.clear()
        ax2.set_title('SIR model')
        ax2.set_xlim(0,timer_tab2)
        ax2.set_ylim(0,95)
        
        ax2.plot(ys2,xs2, label='N_Infected', color = 'red')
        ax2.plot(ys2,xsus2, label='N_Susceptible', color = 'blue')
        ax2.plot(ys2,xrec2, label='N_Recovered', color = 'green')

        ax2.legend()
        
        graph2.draw()

    def animate3(infected, timer_tab3, susceptible,recovered, n_people):
        # Add x and y to lists
        xs3.append(infected)
        ys3.append(timer_tab3)
        xsus3.append(susceptible)
        xrec3.append(recovered)

        # Draw x and y lists
        ax3.clear()
        ax3.set_title('SIR model')
        ax3.set_xlim(0,timer_tab3)
        ax3.set_ylim(0,n_people+5)
        
        ax3.plot(ys3,xs3, label='N_Infected', color = 'red')
        ax3.plot(ys3,xsus3, label='N_Susceptible', color = 'blue')
        ax3.plot(ys3,xrec3, label='N_Recovered', color = 'green')

        ax3.legend()
        
        graph3.draw()
    #pocet nakazenych
    def number_of_infected(people,num_tab):
        infected = 0
        for p in people:
            if(p.tab == num_tab):
                if(p.color == "red" or p.color == "yellow"):
                    infected += 1
        return infected

    #pocet vyliecenych
    def number_of_recovered(people,num_tab):
        recovered = 0
        for p in people:
            if(p.tab == num_tab):
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
    def spawn_people(n,diameter,num_tab,min_x,min_y,max_x,max_y,window,max_speed):
        forbidden_spawn_coords = [[300,300,345,345]]
        forbidden_spawn_coords2 = []
        forbidden_spawn_coords3 = []
        for i in range(0,n):        
            passed = False
            while(not passed):
                start_x = numpy.random.randint(min_x,max_x)
                start_y = numpy.random.randint(min_y,max_y)
                if(start_x+diameter >= max_x):
                    start_x = start_x - diameter
                if(start_y+diameter >= max_y):
                    start_y = start_y - diameter
                if(num_tab == 1):
                    for coords in forbidden_spawn_coords:
                        if(start_x+diameter < coords[0] or start_y+diameter < coords[1] \
                                or start_x > coords[2] or start_y > coords[3]):
                                passed = True
                        else:
                            passed = False
                            break
                elif(num_tab == 2):
                    if(not forbidden_spawn_coords2):
                        passed = True
                    else:
                        for coords in forbidden_spawn_coords2:
                            if(start_x+diameter < coords[0] or start_y+diameter < coords[1] \
                                or start_x > coords[2] or start_y > coords[3]):
                                passed = True
                            else:
                                passed = False
                                break
                elif(num_tab == 3):
                    if(not forbidden_spawn_coords3):
                        passed = True
                    else:
                        for coords in forbidden_spawn_coords3:
                            if(start_x+diameter < coords[0] or start_y+diameter < coords[1] \
                                or start_x > coords[2] or start_y > coords[3]):
                                passed = True
                            else:
                                passed = False
                                break

            if(passed):
                if(num_tab == 1):
                    forbidden_spawn_coords.append([start_x,start_y,start_x+diameter,start_y+diameter])

                    ball = canvas.create_oval(start_x, start_y,start_x+diameter, start_y+diameter, outline="black",
                                fill="blue", width=2)
                    
                    human = Human(diameter,start_x+diameter/2,start_y+diameter/2,0,ball,start_x,start_y,"blue",True,0,start_x,start_y,num_tab,window=window)
                    human.prob_of_pos_test = random.randint(0,100)
                    move_x,move_y = 0,0
                    while(move_x == 0 and move_y == 0):
                        move_x = numpy.random.randint(-max_speed,max_speed)
                        move_y = numpy.random.randint(-max_speed,max_speed)
                    human.xspeed = move_x
                    human.yspeed = move_y
                    people.append(human)
                elif(num_tab == 2):
                    forbidden_spawn_coords2.append([start_x,start_y,start_x+diameter,start_y+diameter])

                    ball = canvas2.create_oval(start_x, start_y,start_x+diameter, start_y+diameter, outline="black",
                                fill="blue", width=2)
                    
                    human = Human(diameter,start_x+diameter/2,start_y+diameter/2,0,ball,start_x,start_y,"blue",True,0,start_x,start_y,num_tab,window=window)
                    human.prob_of_pos_test = random.randint(0,100)
                    move_x,move_y = 0,0
                    while(move_x == 0 and move_y == 0):
                        move_x = numpy.random.randint(-max_speed,max_speed)
                        move_y = numpy.random.randint(-max_speed,max_speed)
                    human.xspeed = move_x
                    human.yspeed = move_y
                    people2.append(human)
                elif(num_tab == 3):
                    forbidden_spawn_coords3.append([start_x,start_y,start_x+diameter,start_y+diameter])

                    ball = canvas3.create_oval(start_x, start_y,start_x+diameter, start_y+diameter, outline="black",
                                fill="blue", width=2)
                    
                    human = Human(diameter,start_x+diameter/2,start_y+diameter/2,0,ball,start_x,start_y,"blue",True,0,start_x,start_y,num_tab,window=window)
                    human.prob_of_pos_test = random.randint(0,100)
                    move_x,move_y = 0,0
                    while(move_x == 0 and move_y == 0):
                        move_x = numpy.random.randint(-max_speed,max_speed)
                        move_y = numpy.random.randint(-max_speed,max_speed)
                    human.xspeed = move_x
                    human.yspeed = move_y
                    people3.append(human)
                
    # testovanie vsetkych ludi okrem karanteny
    def test_everyone():
        sample_size = round((n_people/100)*sample_slider.get())
        sample_of_people = random.sample(people,sample_size)
        for p in sample_of_people:
            if((p.color == "red" or p.color == "yellow") and p.in_quarantine == False):
                if(random.randint(0,100) < p.prob_of_pos_test):
                    p.prob_to_quar = 1
                    p.prob_from_quar = 0
                    p.move_to_quarantine(canvas,testing = True)

    def test_everyone2():
        sample_size = round((90/100)*sample_slider2.get())
        sample_of_people = random.sample(people2,sample_size)
        for p in sample_of_people:
            if((p.color == "red" or p.color == "yellow") and p.in_quarantine == False):
                if(random.randint(0,100) < p.prob_of_pos_test):
                    p.prob_to_quar = 1
                    p.prob_from_quar = 0
                    p.move_to_quarantine(canvas2,testing = True)
    #testovanie ludi v karantene
    def test_people_in_quarantine():
        for p in people:
            if(p.in_quarantine == True and p.color != "red" and p.color != "yellow"):
                p.prob_from_quar = 1
                p.move_from_quarantine(canvas)

    def test_people_in_quarantine2():
        for p in people2:
            if(p.in_quarantine == True and p.color != "red" and p.color != "yellow"):
                p.prob_from_quar = 1
                p.move_from_quarantine(canvas2)
    # spocitanie ludi v karantene
    def number_of_people_in_quarantine(people):
        number = 0
        for p in people:
            if(p.in_quarantine == True):
                number += 1
        return number

    def configure_people(ppl,size_of_sample,pof):
        sample_size = round((len(ppl)/100)*size_of_sample)
        sample = random.sample(ppl,sample_size)
        ppl_without_rules = []
        for p in sample:
            if(p not in ppl_without_rules):
                p.rules_apply = False
                p.prob_of_infection = 30
                ppl_without_rules.append(p)

        for p in ppl:
            p.prob_of_infection += pof
            p.last_prob = p.prob_of_infection

    spawn_people(n=n_people,diameter=diameter,num_tab=1, min_x = bounds_x_main[0], min_y = bounds_y_main[0], max_x = bounds_x_main[1]-2, max_y = bounds_y_main[1],window=1,max_speed=Settings_Tab1['max_speed'])

    for i in range(0,9):
        bounds_x = bounds_x_main2[i]
        bounds_y = bounds_y_main2[i]
        spawn_people(n=10,diameter=diameter,num_tab=2,min_x=bounds_x[0], min_y=bounds_y[0], max_x=bounds_x[1], max_y = bounds_y[1],window=i,max_speed=Settings_Tab1['max_speed'])


    ##TAB 3 ###
    bx = bounds_x_dict[Settings_Tab1['n_areas']]
    by = bounds_y_dict[Settings_Tab1['n_areas']]
    n_ppl_area = 0
    mod = Settings_Tab1['n_people'] % Settings_Tab1['n_areas']
    if(mod == 0):
        n_ppl_area = Settings_Tab1['n_people']/Settings_Tab1['n_areas']
    else:
        n_ppl_area = (Settings_Tab1['n_people']-mod)/Settings_Tab1['n_areas']
        for i in range(mod):
            p = random.randint(0,Settings_Tab1['n_areas']-1)
            bounds_x = bx[p]
            bounds_y = by[p]
            spawn_people(n=1,diameter=diameter,num_tab=3,min_x=bounds_x[0], min_y=bounds_y[0], max_x=bounds_x[1], max_y = bounds_y[1],window=p,max_speed=Settings_Tab1['max_speed'])

    
    for i in range(0,Settings_Tab1['n_areas']):
        bounds_x = bx[i]
        bounds_y = by[i]
        spawn_people(n=int(n_ppl_area),diameter=diameter,num_tab=3,min_x=bounds_x[0], min_y=bounds_y[0], max_x=bounds_x[1], max_y = bounds_y[1],window=i,max_speed=Settings_Tab1['max_speed'])


    configure_people(people3,Settings_Tab1['rules_sample'],Settings_Tab1['prob_of_infection'])
####################


    # print(len(people))
    # for p in people:
    #     print('id',p.id_,'speed:',p.xspeed,',',p.yspeed)

    ########## MENU ########## 

    ########################################### CANVAS 1 ################################################
    # WIDGET_SLIDER

    widget_slider = Scale(canvas,from_= 0, to = 50, orient=HORIZONTAL)
    widget_slider.set(15)
    widget_slider.pack()
    canvas.create_window(740, 115, window=widget_slider)

    area_slider = widget_slider.get()

    widget_slider2 = Scale(canvas, from_= 0, to = 100, orient=HORIZONTAL)
    widget_slider2.set(20)
    widget_slider2.pack()
    canvas.create_window(740, 155, window=widget_slider2)

    widget_slider3 = Scale(canvas, from_= 0, to = 20, orient=HORIZONTAL)
    widget_slider3.set(5)
    widget_slider3.pack()
    canvas.create_window(740, 195, window=widget_slider3)
    #slider pre velkost samplu na testovanie
    sample_slider = Scale(canvas, from_= 1, to = 100, orient=HORIZONTAL)
    sample_slider.set(50)
    sample_slider.pack()
    canvas.create_window(740, 35, window=sample_slider)

    p_rules_slider = Scale(canvas, from_= 1, to = 100, orient=HORIZONTAL)
    p_rules_slider.set(50)
    p_rules_slider.pack()
    canvas.create_window(740, 75, window=p_rules_slider)

    # WIDGET_LABELS
    widget_title = Label(canvas, text='Settings')
    widget_title.pack()
    canvas.create_window(670, 10, window=widget_title)

    widget_label = Label(canvas, text='Number of people in central area: 0')
    widget_label.pack()
    canvas.create_window(656, 230, window=widget_label)  

    widget_label2 = Label(canvas, text='Infection area of effect:')
    widget_label2.pack()
    canvas.create_window(625, 120, window=widget_label2)

    widget_label3 = Label(canvas, text='Probability of infection:')
    widget_label3.pack()
    canvas.create_window(625, 160, window=widget_label3)

    widget_label4 = Label(canvas, text='Number of people in quarantine: 0')
    widget_label4.pack()
    canvas.create_window(655, 250, window=widget_label4)

    widget_label6 = Label(canvas, text='Social distancing size:')
    widget_label6.pack()
    canvas.create_window(620, 200, window=widget_label6)
    
    widget_label7 = Label(canvas, text='Testing of people(%):')
    widget_label7.pack()
    canvas.create_window(620, 40, window=widget_label7)

    widget_label8 = Label(canvas, text='Violation of rules(%):')
    widget_label8.pack()
    canvas.create_window(620, 80, window=widget_label8)

    # CHECK_BUTTONS
    chcek_button1_status = IntVar()
    check_button1 = Checkbutton(canvas, text='Soc. dist.', variable=chcek_button1_status)
    check_button1.pack()
    canvas.create_window(600, 270, window=check_button1)

    testing_button = Button(canvas,text = "Testing", command = test_everyone)
    canvas.create_window(600,295,window = testing_button)

    quarantine_button = Button(canvas,text = "Quarantine", command = test_people_in_quarantine)
    canvas.create_window(670,295,window = quarantine_button)

    ######################################### Canvas 2 #######################################
    # WIDGET_SLIDER

    widget_slider4 = Scale(canvas2,from_= 0, to = 50, orient=HORIZONTAL)
    widget_slider4.set(15)
    widget_slider4.pack()
    canvas2.create_window(200, 670, window=widget_slider4)

    area_slider2 = widget_slider.get()

    widget_slider5 = Scale(canvas2, from_= 0, to = 100, orient=HORIZONTAL)
    widget_slider5.set(20)
    widget_slider5.pack()
    canvas2.create_window(445, 670, window=widget_slider5)

    widget_slider6 = Scale(canvas2, from_= 0, to = 20, orient=HORIZONTAL)
    widget_slider6.set(5)
    widget_slider6.pack()
    canvas2.create_window(680, 670, window=widget_slider6)

    widget_slider7 = Scale(canvas2, from_= 0, to = 10, orient=HORIZONTAL)
    widget_slider7.set(1)
    widget_slider7.pack()
    canvas2.create_window(850, 670, window=widget_slider7)

    sample_slider2 = Scale(canvas2, from_= 1, to = 100, orient=HORIZONTAL)
    sample_slider2.set(50)
    sample_slider2.pack()
    canvas2.create_window(870, 30, window=sample_slider2)

    p_rules_slider2 = Scale(canvas2, from_= 1, to = 100, orient=HORIZONTAL)
    p_rules_slider2.set(50)
    p_rules_slider2.pack()
    canvas2.create_window(870, 90, window=p_rules_slider2)

    # WIDGET_LABELS

    widget_label9 = Label(canvas2, text='Infection area of effect:')
    widget_label9.pack()
    canvas2.create_window(92, 677, window=widget_label9)

    widget_label10 = Label(canvas2, text='Probability of infection:')
    widget_label10.pack()
    canvas2.create_window(335, 677, window=widget_label10)

    widget_label11 = Label(canvas2, text='Number of people in quarantine: 0')
    widget_label11.pack()
    canvas2.create_window(600, 640, window=widget_label11)

    widget_label12 = Label(canvas2, text='Probability of infection (%): 0')
    widget_label12.pack()
    canvas2.create_window(350, 640, window=widget_label12)

    widget_label13 = Label(canvas2, text='Social distancing size:')
    widget_label13.pack()
    canvas2.create_window(566, 677, window=widget_label13)

    widget_label14 = Label(canvas2, text='Turists:')
    widget_label14.pack()
    canvas2.create_window(780, 677, window=widget_label14)

    # CHECK_BUTTONS
    chcek_button2_status = IntVar()
    check_button2 = Checkbutton(canvas2, text='Soc. dist.', variable=chcek_button2_status)
    check_button2.pack()
    canvas2.create_window(750, 640, window=check_button2)

    # BUTTON
    testing_button2 = Button(canvas2,text = "Testing", command = test_everyone2)
    canvas2.create_window(850,640,window = testing_button2)

    quarantine_button2 = Button(canvas2,text = "Quarantine", command = test_people_in_quarantine2)
    canvas2.create_window(950,640,window = quarantine_button2)

    ####### END OF MENU ######

    tabID = notebook.index(notebook.select())

    print(len(people),len(people2))

    while 1:
        #print('Settings:\nN_PPL:{}\nQuar:{}\nSD:{}\nAreas:{}'.format(Settings_Tab1['n_people'],Settings_Tab1['quarantine'],Settings_Tab1['social_distancing'],Settings_Tab1['n_areas']))
        tabID=notebook.index(notebook.select())
        # choice one human, who will be infectioned
        if(timer_tab1 == 10):
            infected_id_tab1 = numpy.random.randint(people[0].id_,people[n_people-1].id_)
            num_infected += 1
            for p in people:
                if(p.id_ == infected_id_tab1):
                    p.color = "red"
                
        if(timer_tab2 == 10):
            infected_id_tab2 = numpy.random.randint(people2[0].id_,people2[len(people2)-1].id_)
            num_infected += 1
            for p in people2:
                if(p.id_ == infected_id_tab2):
                    p.color = "red"

        if(timer_tab3 == 10):
            infected_id_tab3 = numpy.random.randint(people3[0].id_,people3[len(people3)-1].id_)
            num_infected += 1
            for p in people3:
                if(p.id_ == infected_id_tab3):
                    p.color = "red"            

        if(tabID == 0):
            if(loop):
                social_distancing = chcek_button1_status.get()
                area_slider = widget_slider.get()
                probability_slider = widget_slider2.get()
                rules_slider = p_rules_slider.get()

                #if(rules_sample != rules_slider):
                sample_size = round((n_people/100)*rules_slider)
                sample = random.sample(people,sample_size)
                print('ss',sample_size,'pwr',len(ppl_without_rules))
                if(len(ppl_without_rules) < len(sample)):
                    for p in sample:
                        if(p not in ppl_without_rules):
                            p.rules_apply = False
                            ppl_without_rules.append(p)
                        
                elif(len(ppl_without_rules) > len(sample)):
                    n = abs(len(ppl_without_rules) - len(sample))
                    for i in range(n):
                        x = ppl_without_rules.pop(random.randint(0,len(ppl_without_rules)-1))
                        x.rules_apply = True
                else:
                    pass

                    rules_sample = rules_slider

                if(probability != probability_slider):
                    for p in people:
                        p.prob_of_infection = probability_slider
                        probability = probability_slider
                timer_tab1 += 1
                    
                # choice random human and set middle position
                rand_number = random.randint(0,100)
                if(rand_number < 30):
                    if(people[rand_number].in_quarantine == False):
                        people[rand_number].motion = False
                        #x1,y1,_,_ = canvas.coords(people[rand_number].id_)
                        people[rand_number].last_x = people[rand_number].x
                        people[rand_number].last_y = people[rand_number].y
                        people[rand_number].move_self(canvas,bounds_x_central[0]-people[rand_number].x+(16-10)/2,bounds_y_central[0]-people[rand_number].y+(16-10)/2)
                        #canvas.coords(people[rand_number].id_,315,315,315+diameter,315+diameter)

                n_people_in_area = 0
                for p in people:
                    if(p.tab == 1):
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
                        if(p.color == "red" or p.color == "yellow"):
                            p.setOneMoreDay()
                            p.recover(200)

                        if(p.motion == True):
                            p.border_intersect(bounds_x,bounds_y,canvas)
                            #p.border_intersect2(bounds_x,bounds_y,canvas)
                            p.move_self(canvas)
                        else:
                            p.oneMoreDayNoMotion()

                        if(p.days_no_motion > 20):
                            p.motion = True
                            last_x, last_y = p.getLastPosition()
                            p.days_no_motion = 0
                            p.move_self(canvas,last_x-p.x,last_y-p.y)
                        for n in people:
                            if(n.tab == 1):
                                if(p.in_quarantine == False and n.in_quarantine == False):
                                    if(social_distancing):
                                        distance_slider = widget_slider3.get()
                                        intersecting_aoe = p.social_distancing(area_slider,n,canvas,distance_slider)
                                        #intersecting_aoe = p.social_distancing2(area_slider,n,canvas,distance_slider)
                                    else:
                                        intersecting = p.people_intersect(n,canvas)
                                        #intersecting = p.people_intersect2(n,canvas)
                                    #nakaza
                                    if(intersecting or intersecting_aoe):
                                        if(intersecting):
                                            p.prob_of_infection = 100
                                        else:
                                            p.prob_of_infection = probability_slider
                                        if(n.color =="red" or p.color == "red" or n.color == "yellow" or p.color == "yellow"):
                                            if(not (n.color == "green" or p.color == "green")):
                                                random_number = numpy.random.randint(0,100)
                                                if(p.motion == False):
                                                    p.prob_of_infection += 20
                                                if(random_number <= p.prob_of_infection):
                                                    random_number = numpy.random.randint(0,100)
                                                    if(p.color == "blue"):
                                                        if(random_number <= 70):
                                                            p.color = "red"
                                                        else:
                                                            p.color = "yellow"
                                                    if(n.color == "blue"):
                                                        if(random_number <= 70):
                                                            n.color = "red"
                                                        else:
                                                            n.color = "yellow"
                                                
                widget_label.configure(text='Number of people in central area: {}'.format(n_people_in_area))
                widget_label4.configure(text='Number of people in quarantine: {}'.format(number_of_people_in_quarantine(people))) 
                num_infected = number_of_infected(people,1)
                num_recovered = number_of_recovered(people,1)
                num_sus = n_people - num_infected - num_recovered
                #print("infected: ",num_infected,", time:", timer_tab1)
                if(timer_tab1 % 2 == 0):
                    animate(num_infected,timer_tab1,num_sus,num_recovered,n_people)
            # print('som na tabe1')
        elif(tabID == 1):
            if(loop):
                social_distancing = chcek_button2_status.get()
                area_slider = widget_slider4.get()
                probability_slider = widget_slider5.get()
                number_of_turists = widget_slider7.get()

                rules_slider2 = p_rules_slider2.get()

                if(rules_sample2 != rules_slider2):
                    sample_size = round((len(people2)/100)*rules_slider2)
                    sample = random.sample(people2,sample_size)
                    if(len(ppl_without_rules2) < len(sample)):
                        for p in sample:
                            if(p not in ppl_without_rules2):
                                p.rules_apply = False
                                ppl_without_rules2.append(p)
                            
                    elif(len(ppl_without_rules2) > len(sample)):
                        n = abs(len(ppl_without_rules2) - len(sample))
                        for i in range(n):
                            x = ppl_without_rules2.pop(random.randint(0,len(ppl_without_rules2)-1))
                            x.rules_apply = True
                    else:
                        pass

                    rules_sample2 = rules_slider2


                if(probability != probability_slider):
                    for p in people2:
                        p.prob_of_infection = probability_slider
                        probability = probability_slider
                timer_tab2 += 1
                    
                for i in range(0,number_of_turists):
                    done = False
                    while(done == False):
                        random_human = numpy.random.randint(people2[0].id_,people2[len(people2)-1].id_)
                        for p in people2:
                            if(p.id_ == random_human and p.tab == 2):
                                random_window = numpy.random.randint(0,8)
                                window = bounds_x_main2[random_window]
                                p.move_self(canvas2,window[0]-125,window[1]-95)
                                done = True
                                p.window = random_window
                                break
                    

                for p in people2:
                    if(p.tab == 2):
                        if(p.color == "red"):
                            p.prob_to_quar = 0.01
                            p.prob_from_quar = 0
                            p.move_to_quarantine(canvas2)
                        else:
                            p.prob_to_quar = 0
                            p.prob_from_quar = 0.1
                            p.move_from_quarantine(canvas2)
                        if(p.in_quarantine):
                            bounds_x = bounds_x_quar2
                            bounds_y = bounds_y_quar2
                        else:
                            bounds_x = bounds_x_main2[p.window]
                            bounds_y = bounds_y_main2[p.window]

                        canvas2.itemconfig(p.id_,fill=p.color)
                        if(p.color == "red" or p.color == "yellow"):
                            p.setOneMoreDay()
                            p.recover(200)

                        if(p.motion == True):
                            p.border_intersect2(bounds_x,bounds_y,canvas2)
                            p.move_self(canvas2)
                        else:
                            p.oneMoreDayNoMotion()

                        if(p.days_no_motion > 20):
                            p.motion = True
                            last_x, last_y = p.getLastPosition()
                            p.days_no_motion = 0
                            p.move_self(canvas2,last_x-p.x,last_y-p.y)
                        for n in people2:
                            if(n.tab == 2):
                                if(p.in_quarantine == False and n.in_quarantine == False):
                                    if(social_distancing):
                                        distance_slider = widget_slider3.get()
                                        intersecting_aoe = p.social_distancing(area_slider,n,canvas2,distance_slider)
                                        #intersecting_aoe = p.social_distancing2(area_slider,n,canvas2,distance_slider)
                                    else:
                                        #intersecting = p.people_intersect2(n,canvas2)
                                        intersecting = p.people_intersect(n,canvas2)
                                    #nakaza
                                    if(intersecting or intersecting_aoe):
                                        if(intersecting):
                                            p.prob_of_infection = 100
                                        else:
                                            p.prob_of_infection = probability_slider
                                        if(n.color =="red" or p.color == "red" or n.color == "yellow" or p.color == "yellow"):
                                            if(not (n.color == "green" or p.color == "green")):
                                                random_number = numpy.random.randint(0,100)
                                                if(p.motion == False):
                                                    p.prob_of_infection += 20
                                                if(random_number <= p.prob_of_infection):
                                                    random_number = numpy.random.randint(0,100)
                                                    if(p.color == "blue"):
                                                        if(random_number <= 70):
                                                            p.color = "red"
                                                        else:
                                                            p.color = "yellow"
                                                    if(n.color == "blue"):
                                                        if(random_number <= 70):
                                                            n.color = "red"
                                                        else:
                                                            n.color = "yellow"
        elif(tabID == 2):
            if(loop):
                timer_tab3 += 1
                
                if(Settings_Tab1['mobility']):
                    done = False
                    while(done == False):
                        random_human = numpy.random.randint(people3[0].id_,people3[len(people3)-1].id_)
                        for p in people3:
                            if(p.id_ == random_human and p.tab == 3):
                                random_window = random.randint(0,Settings_Tab1['n_areas']-1)
                                if(p.window != random_window):
                                    window_x = bx[random_window]
                                    window_y = by[random_window]
                                    window_w = abs(window_x[0]-window_x[1])
                                    window_h = abs(window_y[0]-window_y[1])

                                    p.move_self(canvas3,(window_x[0]+window_w/2)-p.x,(window_y[0]+window_h/2)-p.y)
                                    done = True
                                    p.window = random_window
                                break
                    
                for p in people3:
                    if(p.tab == 3):
                        if(Settings_Tab1['quarantine']):
                            if(p.color == "red"):
                                p.prob_to_quar = 0.01
                                p.prob_from_quar = 0
                                p.move_to_quarantine(canvas3)
                            else:
                                p.prob_to_quar = 0
                                p.prob_from_quar = 0.1
                                p.move_from_quarantine(canvas3)

                        if(p.in_quarantine and Settings_Tab1['quarantine']):
                            bounds_x = bxq
                            bounds_y = byq
                        else:
                            bounds_x = bx[p.window]
                            bounds_y = by[p.window]

                        canvas3.itemconfig(p.id_,fill=p.color)
                        if(p.color == "red" or p.color == "yellow"):
                            p.setOneMoreDay()
                            p.recover(200)

                        if(p.motion == True):
                            p.border_intersect(bounds_x,bounds_y,canvas3)
                            p.move_self(canvas3)
                        else:
                            p.oneMoreDayNoMotion()

                        if(p.days_no_motion > 20):
                            p.motion = True
                            last_x, last_y = p.getLastPosition()
                            p.days_no_motion = 0
                            p.move_self(canvas3,last_x-p.x,last_y-p.y)
                        for n in people3:
                            if(n.tab == 3):
                                if(p.in_quarantine == False and n.in_quarantine == False):
                                    if(Settings_Tab1['social_distancing']):
                                        #TODODODODODODODODOD#
                                        distance_slider = widget_slider3.get()
                                        #################################
                                        intersecting_aoe = p.social_distancing(Settings_Tab1['size_of_infection_area'],n,canvas3,distance_slider)
                                        #intersecting_aoe = p.social_distancing2(area_slider,n,canvas2,distance_slider)
                                    else:
                                        #intersecting = p.people_intersect2(n,canvas2)
                                        intersecting = p.people_intersect(n,canvas3)
                                    
                                    infectious_area = p.in_infectious_area(Settings_Tab1['size_of_infection_area'],n,canvas3)
                                    #nakaza
                                    if(intersecting or intersecting_aoe or infectious_area and (p.window == n.window)):
                                        if(intersecting):
                                            p.last_prob = p.prob_of_infection
                                            p.prob_of_infection = 100
                                        else:
                                            p.prob_of_infection = p.last_prob
                                        if(n.color =="red" or p.color == "red" or n.color == "yellow" or p.color == "yellow"):
                                            if(not (n.color == "green" or p.color == "green")):
                                                random_number = numpy.random.randint(0,100)
                                                if(p.motion == False):
                                                    p.prob_of_infection += 20
                                                if(random_number <= p.prob_of_infection):
                                                    random_number = numpy.random.randint(0,100)
                                                    if(p.color == "blue"):
                                                        if(random_number <= 70):
                                                            p.color = "red"
                                                        else:
                                                            p.color = "yellow"
                                                    if(n.color == "blue"):
                                                        if(random_number <= 70):
                                                            n.color = "red"
                                                        else:
                                                            n.color = "yellow"
            
                                                
                num_infected = number_of_infected(people3,3)
                num_recovered = number_of_recovered(people3,3)
                num_sus = Settings_Tab1['n_people'] - num_infected - num_recovered
                #print("infected: ",num_infected,", time:", timer_tab1)
                if(timer_tab3 % 2 == 0):
                    animate3(num_infected,timer_tab3,num_sus,num_recovered,Settings_Tab1['n_people'])
            # print('som na tabe2')


        if keyboard.is_pressed('q'):
            if(loop == True):
                loop = False
            else:
                loop = True
        if keyboard.is_pressed('e'):
            break

        time.sleep(0)
        screen.update()
