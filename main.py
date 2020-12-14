from window import Screen
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog as tkFileDialog
from math import *
import numpy, keyboard, time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Human import *
import os,sys
from dicttoxml import *
from xml.etree import ElementTree
from copy import copy
from distutils import util
from reportlab.pdfgen.canvas import Canvas as PDFCanvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units import *
from reportlab.graphics import renderPDF
from io import BytesIO
from svglib.svglib import svg2rlg


##############SETTINGS###################
WINDOW_WIDTH = 1550
WINDOW_HEIGTH = 720

SETTINGS = {'social_distancing' : False,
'quarantine' : False,
'n_people' : 0,
'n_areas' : 0,
'central' : False,
'max_speed' : 10,
'prob_of_infection' : 0,
'size_of_infection_area' : 0,
'rules_sample' : 50,
'mobility' : False,
'p_central' : 0,
'p_mobility' : 0
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
byq = [280, 480]


intersecting_aoe = False
intersecting = False

xs3 = []
ys3 = []

xsus3 = []
xrec3 = []


num_infected = 0
num_sus = 0
num_recovered = 0

people3 = []
diameter = 10

timer_tab3 = 0
question_timer = 0

asked_to_save = False
loop = False
run = True

##############################################

####################################### SETTINGS WINDOW ################################################
SCREEN = Screen('settings',500,800)
screen = SCREEN.screen

settings_window = Frame(screen)
settings_window.pack()
#read settings and save them to dict
def create_world():
    SETTINGS['n_people'] = int(TXT_BOX.get())
    SETTINGS['social_distancing'] = bool(CHCK_BTN2_STATUS.get())
    SETTINGS['quarantine'] = bool(CHCK_BTN1_STATUS.get())
    SETTINGS['n_areas'] = int(TXT_BOX2.get())
    SETTINGS['central'] = bool(CHCK_BTN4_STATUS.get())
    SETTINGS['max_speed'] = int(SLIDER_SPEED.get())
    SETTINGS['prob_of_infection'] = int(SLIDER_POF.get())
    SETTINGS['size_of_infection_area'] = int(SLIDER_AREA.get())
    SETTINGS['p_central'] = int(SLIDER_P_CENTRAL.get())
    if(SETTINGS['n_areas'] > 1):
        SETTINGS['p_mobility'] = int(SLIDER_P_MOBILITY.get())
        SETTINGS['mobility'] = bool(CHCK_BTN3_STATUS.get())
    SETTINGS['rules_sample'] = int(SLIDER_SAMPLE.get())
    settings_window.destroy()
    screen.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGTH))
    SCREEN.name = 'main'

#help func
def dictify(r,root=True):
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d

#load settings from xml
def load_settings():
    ftypes = [('XML FILES','*.xml'), ('All files', '*')]
    dlg = tkFileDialog.Open(filetypes = ftypes)
    fl = dlg.show()
    if(fl != ''):
        print(fl)
    else:
        print("ERROR LOADING FILE")
        return
    file = open(fl)
    if(file is None):
        return
    xml_string = file.read()  

    tree = ElementTree.fromstring(xml_string)

    dictified_tree = dictify(tree)
    SETTINGS['social_distancing'] = bool(util.strtobool(dictified_tree['root']['social_distancing'][0]['_text']))
    SETTINGS['quarantine'] = bool(util.strtobool(dictified_tree['root']['quarantine'][0]['_text']))
    SETTINGS['n_people'] = int(dictified_tree['root']['n_people'][0]['_text'])
    SETTINGS['n_areas'] = int(dictified_tree['root']['n_areas'][0]['_text'])
    SETTINGS['central'] = bool(util.strtobool(dictified_tree['root']['central'][0]['_text']))
    SETTINGS['max_speed'] = int(dictified_tree['root']['max_speed'][0]['_text'])
    SETTINGS['prob_of_infection'] = int(dictified_tree['root']['prob_of_infection'][0]['_text'])
    SETTINGS['size_of_infection_area'] = int(dictified_tree['root']['size_of_infection_area'][0]['_text'])
    SETTINGS['rules_sample'] = int(dictified_tree['root']['rules_sample'][0]['_text'])
    SETTINGS['mobility'] = bool(util.strtobool(dictified_tree['root']['mobility'][0]['_text']))

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

CHCK_BTN4_STATUS = IntVar()
CHCK_BTN4 = Checkbutton(settings_canvas, text='Central Areas', variable=CHCK_BTN4_STATUS)
CHCK_BTN4.place(relx = 0, rely = 0.65)

LABEL7 = Label(settings_canvas, text='Probability of moving to central area(%)')
LABEL7.place(relx = 0, rely = 0.7)

SLIDER_P_CENTRAL = Scale(settings_canvas,from_= 0, to = 100, orient=HORIZONTAL)
SLIDER_P_CENTRAL.set(20)
SLIDER_P_CENTRAL.place(relx = 0, rely = 0.72)

LABEL8 = Label(settings_canvas, text='Probability of moving to another area(%)')
LABEL8.place(relx = 0, rely = 0.78)

SLIDER_P_MOBILITY = Scale(settings_canvas,from_= 0, to = 100, orient=HORIZONTAL)
SLIDER_P_MOBILITY.set(20)
SLIDER_P_MOBILITY.place(relx = 0, rely = 0.8)


generate_btn = Button(settings_canvas,text = "GENERATE", command = create_world)
generate_btn.place(relx = 0.3, rely = 0.95)

load_btn = Button(settings_canvas,text = "LOAD SETTINGS", command = load_settings)
load_btn.place(relx = 0.5, rely = 0.95)

while(SCREEN.name == 'settings'):
    screen.update()
  
#########################################################################################################

#Funciton to draw areas on canvas
def generate_areas(cnv,n_areas,bx,by,quar,bxq,byq,central):
    b_x = bx[n_areas]
    b_y = by[n_areas]
    for i in range(len(b_x)):
        bounds_x = b_x[i]
        bounds_y = b_y[i]
        if(central):
            cnv.create_rectangle(((bounds_x[0]+bounds_x[1])/2)-9,((bounds_y[0]+bounds_y[1])/2)-9,((bounds_x[0]+bounds_x[1])/2)+9,((bounds_y[0]+bounds_y[1])/2)+9)
        cnv.create_rectangle(bounds_x[0],bounds_y[0],bounds_x[1],bounds_y[1])
    if(quar):
        cnv.create_rectangle(bxq[0],byq[0],bxq[1],byq[1])


if(SCREEN.name != 'settings'):
    
    notebook = ttk.Notebook(screen)

    tab3 = Frame(notebook)

    notebook.add(tab3, text='Simulation')

    notebook.pack(expand = 1, fill="both")
    
    left_frame_tab3 = Frame(tab3,width=900)
    left_frame_tab3.pack(side=LEFT)

    right_frame_tab3 = Frame(tab3)
    right_frame_tab3.pack(side=RIGHT)
    canvas3 = Canvas(left_frame_tab3, width=900,height=WINDOW_HEIGTH)
    canvas3.pack( side = LEFT)

    cnvq = Canvas(right_frame_tab3,width=650,height=200)
    cnvq.pack(side=BOTTOM)

#call func generate_areas
    generate_areas(canvas3,SETTINGS['n_areas'],bounds_x_dict,bounds_y_dict,SETTINGS['quarantine'],bxq,byq,SETTINGS['central'])
#initialize figure for showing SIR model
    fig3 = plt.Figure(figsize=(8,5), dpi=100)
    ax3 = fig3.add_subplot(111)
    ax3.set_title('SIR model')
    ax3.set_xlim(0,1)
    ax3.set_ylim(0,SETTINGS['n_people']+5)

    ax3.plot(ys3, xs3, label='N_Infected', color = 'red')
    ax3.plot(ys3,xsus3, label='N_Susceptible', color = 'blue')
    ax3.plot(ys3,xrec3, label='N_Recovered', color = 'green')

    ax3.legend()
    graph3 = FigureCanvasTkAgg(fig3,master=right_frame_tab3)
    graph3.get_tk_widget().pack(side="top",fill='both',expand=False)
    #cnvq.create_window(0,0,window=graph3)

    #graf
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
    
    #infected people
    def number_of_infected(people,num_tab):
        infected = 0
        for p in people:
            if(p.tab == num_tab):
                if(p.color == "red" or p.color == "yellow"):
                    infected += 1
        return infected
    
    #recovered people
    def number_of_recovered(people,num_tab):
        recovered = 0
        for p in people:
            if(p.tab == num_tab):
                if(p.color == "green"):
                    recovered += 1
        return recovered

    #spawn people and add them on canvas
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
                if(num_tab == 3):
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
                
    #test people for quarantine
    def test_everyone3():
        sample_size = round((90/100)*widget_slider8.get())
        sample_of_people = random.sample(people3,sample_size)
        for p in sample_of_people:
            if((p.color == "red" or p.color == "yellow") and p.in_quarantine == False):
                if(random.randint(0,100) < p.prob_of_pos_test):
                    p.prob_to_quar = 1
                    p.prob_from_quar = 0
                    p.move_to_quarantine(canvas3,testing = True)
    #test people in quarantine
    def test_people_in_quarantine3():
        for p in people3:
            if(p.in_quarantine == True and p.color != "red" and p.color != "yellow"):
                p.prob_from_quar = 1
                p.move_from_quarantine(canvas3)
    #count ppl in quarantine
    def number_of_people_in_quarantine(people):
        number = 0
        for p in people:
            if(p.in_quarantine == True):
                number += 1
        return number

    #set people probabilities
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
            p.prob_mob = SETTINGS['p_mobility']
            p.prob_central = SETTINGS['p_central']
            p.prob_of_infection += pof
            p.last_prob = p.prob_of_infection

    def sp_simulation():
        global loop
        if(loop):
            loop=False
        else:
            loop=True

    def close_simulation():
        global run
        run = False
        sys.exit()

    def save_settings():
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Settings')
        if not os.path.exists(path):
            os.makedirs(path)
        #print(SETTINGS)
        xml = dicttoxml(SETTINGS)
        f = tkFileDialog.asksaveasfile(mode="w",defaultextension=".xml")
        if(f is None):
            print("file is none")
            return
        f.write(xml.decode("utf8"))
        f.close()
        #print(xml.decode("utf8"))
        
    def save_sim():
        f = tkFileDialog.asksaveasfile(mode="w",defaultextension=".png")
        if(f is None):
            print("file is none")
            return
        print(f.name)
        f.close()
        fig3.savefig(f.name)

    
    def save_whole_simulation(name):
        tp = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Testing')
        if not os.path.exists(tp):
            os.makedirs(tp)
        path = os.path.join(tp,name)
        #first XML
        xml_path = path+".xml"
        xml = dicttoxml(SETTINGS)
        f = open(xml_path,"w")
        if(f is None):
            print("file is none")
            return
        f.write(xml.decode("utf8"))
        f.close()
        #png
        png_path = path+".png"
        fig3.savefig(png_path)

        #pdf
        pdf_path = path+".pdf"
        pdf_canvas = PDFCanvas(pdf_path,pagesize=LETTER)

        settings_string = ["SETTINGS USED:",
        "• Social distancing : {}".format(SETTINGS['social_distancing']),
        "• Quarantine : {}".format(SETTINGS['quarantine']),
        "• Number of people : {}".format(SETTINGS['n_people']),
        "• Number of areas: {}".format(SETTINGS['n_areas']),
        "• Central area : {}".format(SETTINGS['central']),
        "• MAX_SPEED : {}".format(SETTINGS['max_speed']),
        "• Probability of infection: {}".format(SETTINGS['prob_of_infection']),
        "• Size of infectious area(around every individual): {}".format(SETTINGS['size_of_infection_area']),
        "• Sample size of people that do not respect the rules(%): {}".format(SETTINGS['rules_sample']),
        "• Mobility: {}".format(SETTINGS['mobility']),
        "• Probability of traveling between areas: {}".format(SETTINGS['p_mobility']),
        "• Probability of traveling to central area: {}".format(SETTINGS['p_central'])]
        
        x = 1*inch
        y = 10*inch
        pdf_canvas.setFont("Times-Roman", 20)
        for idx,row in enumerate(settings_string):
            if(idx == 1):
                pdf_canvas.setFont("Times-Roman", 10)
                x += 0.1*inch
            pdf_canvas.drawString(x,y,row)            
            y -= 0.2*inch
        
        imgdata = BytesIO()
        temp_fig = fig3
        temp_fig.set_size_inches(6,4)
        temp_fig.savefig(imgdata,format="svg")
        imgdata.seek(0)

        image = svg2rlg(imgdata)

        pdf_canvas.setFont("Times-Roman", 20)
        pdf_canvas.drawString(x-0.1*inch,y-0.1*inch,"OUTPUT GRAPH:")
        renderPDF.draw(image,pdf_canvas,x-0.9*inch,y-5.2*inch)
        pdf_canvas.save()
        #print(path,'\n',xml_path,'\n',png_path,'\n',pdf_path)

    #add people to areas
    bx = bounds_x_dict[SETTINGS['n_areas']]
    by = bounds_y_dict[SETTINGS['n_areas']]
    n_ppl_area = 0
    mod = SETTINGS['n_people'] % SETTINGS['n_areas']
    if(mod == 0):
        n_ppl_area = SETTINGS['n_people']/SETTINGS['n_areas']
    else:
        n_ppl_area = (SETTINGS['n_people']-mod)/SETTINGS['n_areas']
        for i in range(mod):
            p = random.randint(0,SETTINGS['n_areas']-1)
            bounds_x = bx[p]
            bounds_y = by[p]
            spawn_people(n=1,diameter=diameter,num_tab=3,min_x=bounds_x[0], min_y=bounds_y[0], max_x=bounds_x[1], max_y = bounds_y[1],window=p,max_speed=SETTINGS['max_speed'])
    
    for i in range(0,SETTINGS['n_areas']):
        bounds_x = bx[i]
        bounds_y = by[i]
        spawn_people(n=int(n_ppl_area),diameter=diameter,num_tab=3,min_x=bounds_x[0], min_y=bounds_y[0], max_x=bounds_x[1], max_y = bounds_y[1],window=i,max_speed=SETTINGS['max_speed'])

    configure_people(people3,SETTINGS['rules_sample'],SETTINGS['prob_of_infection'])
    ####################

    ########## MENU ########## 
    
    widget_label16 = Label(canvas3, text='Settings')
    widget_label16.pack()
    canvas3.create_window(720, 150, window=widget_label16)
    #150

    # Create widgets, depending on settings
    if(SETTINGS['quarantine'] == True and SETTINGS['social_distancing'] == True):
        # WIDGET_SLIDER
    
        widget_slider8 = Scale(canvas3,from_= 0, to = 100, orient=HORIZONTAL)
        widget_slider8.set(50)
        widget_slider8.pack()
        canvas3.create_window(800, 180, window=widget_slider8)
        #180,220
        widget_slider9 = Scale(canvas3,from_= 0, to = 20, orient=HORIZONTAL)
        widget_slider9.set(5)
        widget_slider9.pack()
        canvas3.create_window(800, 220, window=widget_slider9)
        
        # WIDGET_LABELS

        widget_label13 = Label(canvas3, text='Social distancing size:')
        widget_label13.pack()
        canvas3.create_window(685, 225, window=widget_label13)
        #225,185
        widget_label15 = Label(canvas3, text='Testing of people (%):')
        widget_label15.pack()
        canvas3.create_window(685, 185, window=widget_label15)

        # BUTTON
        testing_button3 = Button(canvas3,text = "Testing", command = test_everyone3)
        canvas3.create_window(650,260,window = testing_button3)
        #260,260
        quarantine_button3 = Button(canvas3,text = "Quarantine", command = test_people_in_quarantine3)
        canvas3.create_window(720,260,window = quarantine_button3)
    elif(SETTINGS['quarantine'] == True and SETTINGS['social_distancing'] == False):
        # WIDGET_SLIDER
    
        widget_slider8 = Scale(canvas3,from_= 0, to = 100, orient=HORIZONTAL)
        widget_slider8.set(50)
        widget_slider8.pack()
        canvas3.create_window(800, 180, window=widget_slider8)
        #180
        # WIDGET_LABELS

        widget_label15 = Label(canvas3, text='Testing of people (%):')
        widget_label15.pack()
        canvas3.create_window(685, 185, window=widget_label15)
        #185
        # BUTTON
        testing_button3 = Button(canvas3,text = "Testing", command = test_everyone3)
        canvas3.create_window(650,225,window = testing_button3)
        #225,225
        quarantine_button3 = Button(canvas3,text = "Quarantine", command = test_people_in_quarantine3)
        canvas3.create_window(720,225,window = quarantine_button3)
    elif(SETTINGS['quarantine'] == False and SETTINGS['social_distancing'] == True):
        
        widget_label13 = Label(canvas3, text='Social distancing size:')
        widget_label13.pack()
        canvas3.create_window(685, 185, window=widget_label13)
        #185,180
        widget_slider9 = Scale(canvas3,from_= 0, to = 20, orient=HORIZONTAL)
        widget_slider9.set(5)
        widget_slider9.pack()
        canvas3.create_window(800, 180, window=widget_slider9)
        
    start_button = Button(canvas3,text = "START/PAUSE", command = sp_simulation)
    canvas3.create_window(720,30,window = start_button)

    exit_button = Button(canvas3,text = "CLOSE", command = close_simulation)
    canvas3.create_window(720,60,window = exit_button)

    save_settings_btn = Button(canvas3,text="EXPORT SETTINGS",command = save_settings)
    canvas3.create_window(720,90,window=save_settings_btn)

    save_simulation = Button(canvas3,text="SAVE SIMULATION GRAPH",command = save_sim)
    canvas3.create_window(720,120,window=save_simulation)
    # 30,60,90,120
    ####### END OF MENU ######
    #MAIN LOOP
    while run:
        # choice one human, who will be infected
        if(timer_tab3 == 10):
            infected_id_tab3 = numpy.random.randint(people3[0].id_,people3[len(people3)-1].id_)
            num_infected += 1
            for p in people3:
                if(p.id_ == infected_id_tab3):
                    p.color = "red"            
        # START/PAUSE
        if(loop):
            timer_tab3 += 1                
            for p in people3:
                #if mobility is on, apply effect of mobility
                if(SETTINGS['mobility']):
                    random_p_mob = random.randint(0,1000)
                    #print(random_p_mob)
                    if(random_p_mob <= p.prob_mob):
                        random_window = random.randint(0,SETTINGS['n_areas']-1)
                        while(random_window == p.window):
                            random_window = random.randint(0,SETTINGS['n_areas']-1)
                        window_x = bx[random_window]
                        window_y = by[random_window]
                        window_w = abs(window_x[0]-window_x[1])
                        window_h = abs(window_y[0]-window_y[1])

                        rand_x = random.randint(int(window_x[0])+10,int(window_x[1])-10)
                        rand_y = random.randint(int(window_y[0])+10,int(window_y[1])-10)

                        p.move_self(canvas3,rand_x-p.x,rand_y-p.y)
                        p.window = random_window

                #if central area is on, apply effect of moving to central areas(shops)
                if(SETTINGS['central']):
                    rand_number = random.randint(0,1000)
                    if(rand_number <= p.prob_central):
                        if(p.in_quarantine == False):
                            p.move_to_center(canvas3,bx[p.window],by[p.window])

                #if infected, small chance to send to quarantine, only if quarantine is on
                if(p.tab == 3):
                    if(SETTINGS['quarantine']):
                        if(p.color == "red"):
                            p.prob_to_quar = 0.01
                            p.prob_from_quar = 0
                            p.move_to_quarantine(canvas3)
                        else:
                            p.prob_to_quar = 0
                            p.prob_from_quar = 0.1
                            p.move_from_quarantine(canvas3)

                    if(p.in_quarantine and SETTINGS['quarantine']):
                        bounds_x = bxq
                        bounds_y = byq
                    else:
                        bounds_x = bx[p.window]
                        bounds_y = by[p.window]

                    canvas3.itemconfig(p.id_,fill=p.color)
                    #recovery after some time, 200 ticks
                    if(p.color == "red" or p.color == "yellow"):
                        p.setOneMoreDay()
                        p.recover(200)

                    #move if not in central area
                    if(p.motion == True):
                        p.border_intersect(bounds_x,bounds_y,canvas3)
                        p.move_self(canvas3)
                    else:
                        p.oneMoreDayNoMotion()
                    #send back from center area
                    if(p.days_no_motion > 20):
                        p.move_from_center(canvas3)
                    for n in people3:
                        if(n.tab == 3):
                            if(p.in_quarantine == False and n.in_quarantine == False):
                                #Social distancing effect
                                if(SETTINGS['social_distancing']):
                                    intersecting_aoe = p.social_distancing(SETTINGS['size_of_infection_area'],n,canvas3,widget_slider9.get())
                                else:
                                    intersecting = p.people_intersecting(n,canvas3)
                                
                                infectious_area = p.in_infectious_area(SETTINGS['size_of_infection_area'],n,canvas3)
                                #infection, depends on probability
                                if(intersecting or intersecting_aoe or infectious_area and (p.window == n.window)):
                                    #if distance between people is too small
                                    if(intersecting):
                                        p.last_prob = p.prob_of_infection
                                        p.prob_of_infection = 100
                                    else:
                                        p.prob_of_infection = p.last_prob
                                    #infect got a 70% chance to get infected with symptomps
                                    if(n.color =="red" or p.color == "red" or n.color == "yellow" or p.color == "yellow"):
                                        if(not (n.color == "green" or p.color == "green")):
                                            random_number = numpy.random.randint(0,100)
                                            if(p.motion == False):
                                                p.last_prob = p.prob_of_infection
                                                p.prob_of_infection += 20
                                            else:
                                                p.prob_of_infection = p.last_prob
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
        
            #graph                                
            num_infected = number_of_infected(people3,3)
            num_recovered = number_of_recovered(people3,3)
            num_sus = SETTINGS['n_people'] - num_infected - num_recovered
            
            if(timer_tab3 % 2 == 0):
                #make graph animated
                animate3(num_infected,timer_tab3,num_sus,num_recovered,SETTINGS['n_people'])
                #check for infected if there is none, ask to save simulation
                if(timer_tab3 > 30 and num_infected == 0 and asked_to_save == False):
                    question_timer += 1
                    if(question_timer > 10):
                        asked_to_save = True
                        loop = False
                        result = tk.messagebox.askyesno("Simulation ended", "Simulation has ended, do you wish to save the simulation output and settings? If no, you can still continue the simulation and save everything manually.")
                        if(result):
                            name = tk.simpledialog.askstring("","Enter name of simulation")
                            save_whole_simulation(name)
                            time.sleep(1)
                            result2 = tk.messagebox.askyesno("","Close simulation?")
                            if(result2):
                                close_simulation()
                            else:
                                loop = True
                        else:
                            loop = True
        
        #time.sleep(0)
        
        screen.update()
