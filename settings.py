WINDOW_WIDTH = 1550
WINDOW_HEIGTH = 720

#####-------TAB 1--------########
social_distancing = True
intersecting_aoe = False
intersecting = False
xs = []
ys = []

xs2 = []
ys2 = []

xsus = []
xrec = []

xsus2 = []
xrec2 = []

n_people = 30
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
diameter = 10

rules_sample = 0
ppl_without_rules = []


number_X = 102
number_Y = 84

timer_tab1 = 0
timer_tab2 = 0

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