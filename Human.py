class Human(object):
    def __init__(self,start_x,start_y,day_of_infection,id_, x , y,color,motion,days_no_motion,last_x,last_y):
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