#-----------------------------------------------------------------------#
#                            BoilerClasses.py                           #
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
# Where all classes used by BoilerGUI are defined including skin info   #
#-----------------------------------------------------------------------#

from Tkinter import *

class Style_Colours:
    def __init__(self):
        self.off = "#25242c"
        self.on = "#d637d2"
        self.bg = "#31343d"
        self.text = "#b4b4c0"
        self.frames = "#0066CC"

class Style_Text:
    def __init__(self):
        self.type = "ubuntu"
        self.med = 16
        self.sml = 10
        self.lrg = 20

class Style:
    def __init__(self):
        self.text = Style_Text()
        self.colours = Style_Colours()        

class Timings:
    def __init__(self,a,b,c,d):
        self.amOn = a
        self.amOff = b
        self.pmOn = c
        self.pmOff = d

class SysState:
    def __init__(self):
        self.isaway = "home"
        self.currentmenu = "home"
        self.boiler = "off"
        self.currentrender = "week"
        self.week = Timings(6.5,  7.0, 16.5, 19.5)
        self.wkd  = Timings(8.0, 10.0, 15.0, 18.0)
        self.away = Timings(0.0,  0.0, 17.0, 18.0)
        self.temp = "20.0"

class TimeArc(Canvas):
    def __init__(self, frame):
        self.radius = 240*4/6/2 - 10
        self.X_Center = 320 / 2
        self.Y_Center = 240*4/6/2
        self.width = 11
        
        style = Style_Colours()
        self.colourOff = style.off
        self.colourOn = style.on

        Canvas.__init__(self, frame, highlightthickness=0)
        
        self.coordCenter = (self.X_Center - self.radius, 
                self.Y_Center - self.radius, 
                self.X_Center + self.radius, 
                self.Y_Center + self.radius)
        
        
        self.coordOff = (self.coordCenter[0] + 320,
                        self.coordCenter[1],
                        self.coordCenter[2] + 320,
                        self.coordCenter[3])
        
        self.coordAM = (self.coordCenter[0] + 320/2 - 10 - self.radius,
                        self.coordCenter[1],
                        self.coordCenter[2] + 320/2 - 10 - self.radius,
                        self.coordCenter[3])
        
        self.coordPM = (self.coordCenter[0] + 320/2 - 10,
                        self.coordCenter[1],
                        self.coordCenter[2] + 320/2 - 10,
                        self.coordCenter[3],)
        
        self.coordSpreadPM = (self.coordCenter[0] - 320 * 1/20,
                            self.coordCenter[1],
                            self.coordCenter[2] - 320 * 1/20,
                            self.coordCenter[3])

        self.coordSpreadAM = (self.coordCenter[0] + 320 * 1/20,
                            self.coordCenter[1],
                            self.coordCenter[2] + 320 * 1/20,
                            self.coordCenter[3])
        
        self.ArcGap = 2
        self.ArcLength = 180 - self.ArcGap * 2
        self.DayNightEnd = -self.ArcLength
        self.NightStart = -(self.ArcLength / 2 + self.ArcGap*2)
        self.DayStart = self.ArcLength / 2

        self.amOff = self.create_arc(self.coordCenter,
                                    start = self.DayStart,
                                    extent = self.DayNightEnd,
                                    style = "arc",
                                    width = self.width,
                                    outline = self.colourOff)
        self.pmOff = self.create_arc(self.coordCenter,
                                    start = self.NightStart,
                                    extent = self.DayNightEnd,
                                    style = "arc", 
                                    width = self.width,
                                    outline = self.colourOff)
        self.amOn = self.create_arc(self.coordCenter,
                                    start = self.DayStart,
                                    extent = self.DayNightEnd,
                                    style = "arc",
                                    width = self.width,
                                    outline = self.colourOn)
        self.pmOn = self.create_arc(self.coordCenter,
                                    start = self.NightStart,
                                    extent = self.DayNightEnd,
                                    style = "arc", 
                                    width = self.width,
                                    outline = self.colourOn)    
    def update(self, times):
        OnDay = times.amOn / 12 * self.ArcLength
        OffDay = times.amOff / 12 * self.ArcLength
        OnNight = (times.pmOn - 12) / 12 * self.ArcLength
        OffNight = (times.pmOff - 12) / 12 * self.ArcLength
        self.itemconfig(self.amOn,
                        start =  self.DayStart - OnDay,
                        extent = OnDay - OffDay)
        self.itemconfig(self.pmOn,
                        start =  self.NightStart - OnNight,
                        extent = OnNight - OffNight)

    def move(self, location, ampm = "am" ):
        animate = False

        if location == "side":
            if ampm == "am":
                newcoordam = self.coordAM
                newcoordpm = self.coordOff
            elif ampm == "pm":
                newcoordam = self.coordOff
                newcoordpm = self.coordPM
        elif location == "center":
            newcoordam = self.coordCenter
            newcoordpm = self.coordCenter
        elif location == "spread":
            newcoordam = self.coordSpreadAM
            newcoordpm = self.coordSpreadPM
        
        if animate == False:
            self.coords(self.amOff,
                        newcoordam[0],
                        newcoordam[1],
                        newcoordam[2],
                        newcoordam[3])
            self.coords(self.pmOff,
                        newcoordpm[0],
                        newcoordpm[1],
                        newcoordpm[2],
                        newcoordpm[3])
            self.coords(self.amOn,
                        newcoordam[0],
                        newcoordam[1],
                        newcoordam[2],
                        newcoordam[3])
            self.coords(self.pmOn,
                        newcoordpm[0],
                        newcoordpm[1],
                        newcoordpm[2],
                        newcoordpm[3])
        