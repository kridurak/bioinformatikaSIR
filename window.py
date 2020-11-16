from tkinter import *

class Screen:
    def __init__(self,name,width,height,title = "Spreading simulation of COVID-19", screen = Tk()):
        self.__init__
        self.screen = screen
        self.width = width
        self.height = height
        self.title = title
        self.name = name
        
        self.screen.geometry(str(self.width)+"x"+str(self.height))
        self.screen.title(self.title)
        