import random
from math import *

class Human(object):
    def __init__(self,diameter,start_x,start_y,day_of_infection,id_, x , y,color,motion,days_no_motion,last_x,last_y):
        self.color = color
        self.id_ = id_
        self.start_x = start_x
        self.start_y = start_y
        self.x = x
        self.y = y
        self.day_of_infection = day_of_infection
        self.motion = motion
        self.days_no_motion = days_no_motion
        self.last_x = last_x
        self.last_y = last_y
        self.xspeed = 0
        self.yspeed = 0
        self.in_quarantine  = False
        self.prob_to_quar = 0
        self.prob_from_quar = 0
        self.prob_of_infection = 0
        self.diameter = diameter

    def setPosition(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPosition(self):
        return self.x, self.y
    
    def setPosition(self,x,y):
        self.x = x
        self.y = y
    
    def setOneMoreDay(self):
        self.day_of_infection += 1
    
    def recover(self, days):
        if(self.day_of_infection >= days):
            self.color = "green"
            
    def oneMoreDayNoMotion(self):
        self.days_no_motion += 1

    def getLastPosition(self):
        return self.last_x, self.last_y

    def move_self(self,canvas):
        canvas.move(self.id_,self.xspeed,self.yspeed)
    
    def border_intersect(self,bounds_x,bounds_y,canvas):
        x1,y1,x2,y2 = canvas.coords(self.id_)
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)
        #1st move to borded then reverse the xspeed and yspeed and move again from the border
        if(x1+self.xspeed < bounds_x[0]):
            if(y1+self.yspeed < bounds_y[0]):
                canvas.move(self.id_,bounds_x[0]-x1,bounds_y[0]-y1)
                self.yspeed *= -1
            elif(y2+self.yspeed> bounds_y[1]):
                canvas.move(self.id_,bounds_x[0]-x1,bounds_y[1]-y2)
                self.yspeed *= -1
            else:    
                canvas.move(self.id_,bounds_x[0]-x1,self.yspeed)
            self.xspeed *= -1
            #canvas.move(infected_id,move_x,move_y)
        elif(x2+self.xspeed > bounds_x[1]):
            if(y1+self.yspeed < bounds_y[0]):
                canvas.move(self.id_,bounds_x[1]-x2,bounds_y[0]-y1)
                self.yspeed *= -1
            elif(y2+self.yspeed > bounds_y[1]):
                canvas.move(self.id_,bounds_x[1]-x2,bounds_y[1]-y2)
                self.yspeed *= -1
            else:    
                canvas.move(self.id_,bounds_x[1]-x2,self.yspeed)
            self.xspeed *= -1
        else:
            if(y1+self.yspeed < bounds_y[0]):
                canvas.move(self.id_,self.xspeed,bounds_y[0]-y1)
                self.yspeed *= -1
            elif(y2+self.yspeed > bounds_y[1]):
                canvas.move(self.id_,self.xspeed,bounds_y[1]-y2)
                self.yspeed *= -1

    def people_intersect(self,n,canvas):
        if(self.motion and n.motion and self.in_quarantine == False):
            intersecting = False
            x1,y1,x2,y2 = canvas.coords(self.id_)
            x1=int(x1)
            x2=int(x2)
            y1=int(y1)
            y2=int(y2)
            #1st ball middle coords
            middle_x = x1 + (self.diameter/2)
            middle_y = y1 + (self.diameter/2)

            if(n != self):
                nx1,ny1,nx2,ny2 = canvas.coords(n.id_)
                nx1=int(nx1)
                nx2=int(nx2)
                ny1=int(ny1)
                ny2=int(ny2)
                #2nd ball middle coords
                middle_nx = nx1 + (n.diameter/2)
                middle_ny = ny1 + (n.diameter/2)

                centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))

                if(centers_distance <= self.diameter):
                    # print('tukli sa')
                    distance_x = abs(middle_nx-middle_x)
                    distance_y = abs(middle_x-middle_y)
                    if (distance_x <= distance_y):
                        intersecting = True
                            

                        if ((self.yspeed > 0 and y1 < ny1) or (self.yspeed < 0 and y1 > ny1)):
                            self.yspeed = -self.yspeed


                        if ((n.yspeed > 0 and ny1 < y1) or (n.yspeed < 0 and ny1 > y1)):
                            n.yspeed = -n.yspeed



                    elif (distance_x > distance_y):
                        if ((self.xspeed > 0 and x1 < nx1) or (self.xspeed < 0 and x1 > nx1)):
                            self.xspeed = -self.xspeed

                        if ((n.xspeed > 0 and nx1 < x1) or (n.xspeed < 0 and nx1 > x1)):
                            n.xspeed = -n.xspeed
            return intersecting

    def social_distancing(self,R,n,canvas,distance):
        if(self.motion and n.motion and self.in_quarantine == False):
            intersecting = False
            x1,y1,x2,y2 = canvas.coords(self.id_)
            x1=int(x1)
            x2=int(x2)
            y1=int(y1)
            y2=int(y2)
            #1st ball middle coords
            middle_x = x1 + (self.diameter/2)
            middle_y = y1 + (self.diameter/2)
            if(n != self):
                nx1,ny1,nx2,ny2 = canvas.coords(n.id_)
                nx1=int(nx1)
                nx2=int(nx2)
                ny1=int(ny1)
                ny2=int(ny2)
                #2nd ball middle coords
                middle_nx = nx1 + (n.diameter/2)
                middle_ny = ny1 + (n.diameter/2)

                centers_distance = sqrt(((middle_x-middle_nx)*(middle_x-middle_nx))+((middle_ny-middle_y)*(middle_ny-middle_y)))
                if(centers_distance <= self.diameter+distance):
                    distance_x = abs(middle_nx-middle_x)
                    distance_y = abs(middle_x-middle_y)
                    if(distance_x > distance_y):
                        if(middle_y > middle_ny):
                            canvas.move(self.id_,0,25-distance_y)
                        else:
                            canvas.move(self.id_,0,(25-distance_y)*-1)
                    else:
                        if(middle_x > middle_nx):
                            canvas.move(self.id_,25-distance_x,0)
                        else:
                            canvas.move(self.id_,(25-distance_x)*-1,0)

                if(centers_distance <= self.diameter+R):
                    intersecting = True
                return intersecting

    def move_to_quarantine(self,canvas):
        if(not self.in_quarantine and self.color == "red"):
            num = random.randint(0,100)
            
            if(num <= self.prob_to_quar*100):
                self.last_x,self.last_y,_,_ = canvas.coords(self.id_)
                canvas.coords(self.id_,625+325/2,250+370/2,625+325/2+self.diameter,250+370/2+self.diameter)
                self.in_quarantine = True

    def move_from_quarantine(self,canvas):
        if(self.in_quarantine and self.color == "green"):
            num = random.randint(0,100)
            if(num <= self.prob_from_quar*100):
                canvas.coords(self.id_,self.last_x,self.last_y,self.last_x+self.diameter,self.last_y+self.diameter)
                self.in_quarantine = False