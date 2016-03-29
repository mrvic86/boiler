#-----------------------------------------------------------------------#
#                            BOILERGUI.py                               #
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
# main code for running the GUI and managing timings                    #
#-----------------------------------------------------------------------#

from Tkinter import *
#from pillow import ImageTk, Image
import time
import BoilerClasses

WinWidth = 320
WinHeight = 240
buttonWidth = 70
buttonHeight = 50
buttonLine = 4
Padding = 10 
MidFrameRows = 7 -1  
buttonSize = WinWidth / 4

def setupStyle():
#-----------------------------------------------------------------------#
# configures GUI for skin from BoilerClasses.py                         #
#-----------------------------------------------------------------------#
    skin = BoilerClasses.Style()
    root.option_add('*Font', skin.text.type)
    root.option_add('*Foreground', skin.colours.text)
    root.option_add('*background', skin.colours.bg)
    return skin

def updateHeader():
#-----------------------------------------------------------------------#
# Updates section at top with system time and date                      #
#-----------------------------------------------------------------------#
    oldtimehour = lblTimeHour.cget("text")
    oldtimemin  = lblTimeMin.cget( "text")
    newtimehour = time.strftime('%H')
    newtimemin  = time.strftime('%M')
    if oldtimemin <> newtimemin:
        lblTimeHour.config(text=newtimehour)
        lblTimeMin.config(text=newtimemin)
        lblDate.config(text=time.strftime("%d/%m/%y"))
        lblDay.config(text=time.strftime("%A"))
    
    if lblTimeCol.cget("text") == ":":
        lblTimeCol.config(text=" ")
    else:
        lblTimeCol.config(text=":")

def updateArcs():
#-----------------------------------------------------------------------#
# Redraws the arc ontimes                                               #
#-----------------------------------------------------------------------#
    if sysdata.currentrender == "week":
        timingArcs.update(sysdata.week)
    elif sysdata.currentrender == "wkd":
        timingArcs.update(sysdata.wkd)
    elif sysdata.currentrender == "away":
        timingArcs.update(sysdata.away)
    return 0

def updateTimings(onoff, delta):
    
    oldOnTime  = int(lblOnHours.cget( "text")) + int(lblOnMins.cget( "text"))/60.0 
    oldOffTime = int(lblOffHours.cget("text")) + int(lblOffMins.cget("text"))/60.0
    newOnTime  = oldOnTime  + delta
    newOffTime = oldOffTime + delta
    
    if sysdata.currentmenu == "am" :
        if newOnTime  < 0  : newOnTime  = 0
        if newOnTime  > 12 : newOnTime  = 12
        if newOffTime < 0  : newOffTime = 0
        if newOffTime > 12 : newOffTime = 12
    else:
        if newOnTime  < 12 : newOnTime  = 12
        if newOnTime  > 24 : newOnTime  = 24
        if newOffTime < 12 : newOffTime = 12
        if newOffTime > 24 : newOffTime = 24
    
    if onoff == "on":
        if newOnTime  > oldOffTime : newOnTime = oldOffTime
    else:
        if newOffTime < oldOnTime  : newOffTime = oldOnTime
    
    if sysdata.currentrender == "week":
        if sysdata.currentmenu == "am":
            if onoff == "on":
                sysdata.week.amOn = newOnTime
            else:
                sysdata.week.amOff = newOffTime
        elif sysdata.currentmenu == "pm":
            if onoff == "on":
                sysdata.week.pmOn = newOnTime
            else:
                sysdata.week.pmOff = newOffTime
                
    elif sysdata.currentrender == "wkd":
        if sysdata.currentmenu == "am":
            if onoff == "on":
                sysdata.wkd.amOn = newOnTime
            else:
                sysdata.wkd.amOff = newOffTime
        elif sysdata.currentmenu == "pm":
            if onoff == "on":
                sysdata.wkd.pmOn = newOnTime
            else:
                sysdata.wkd.pmOff = newOffTime
                
    elif sysdata.currentrender == "away":
        if sysdata.currentmenu == "am":
            if onoff == "on":
                systemdata.away.amOn = newOnTime
            else:
                systemdata.away.amOff = newOffTime
        elif sysdata.currentmenu == "pm":
            if onoff == "on":
                systemdata.away.pmOn = newOnTime
            else:
                systemdata.away.pmOff = newOffTime
    return 0
def updateEditLabels(ampm):
    if sysdata.currentrender == "week":
        timings = sysdata.week
    elif sysdata.currentrender == "wkd":
        timings = sysdata.wkd
    elif sysdata.currentrender == "away":
        timings = sysdata.away
    if ampm == "am":
        lblOnHours.config(text  = str( int(timings.amOn) ))
        lblOnMins.config(text   = str( int((timings.amOn - int(timings.amOn))*60)).zfill(2))
        lblOffHours.config(text = str( int(timings.amOff) ))
        lblOffMins.config(text  = str( int((timings.amOff - int(timings.amOff))*60)).zfill(2))
    elif ampm == "pm":
        lblOnHours.config(text  = str( int(timings.pmOn) ))
        lblOnMins.config(text   = str( int((timings.pmOn - int(timings.pmOn))*60)).zfill(2))
        lblOffHours.config(text = str( int(timings.pmOff) ))
        lblOffMins.config(text  = str( int((timings.pmOff - int(timings.pmOff))*60)).zfill(2))
    return 0
def clickbtnAway(event=0):
    return 0

def clickbtnSys(event=0):
    if sysdata.boiler == "on":
        turnBoiler("off")
    else:
        turnBoiler("on")
    return 0

def clickbtnWeek(event=0):
#-----------------------------------------------------------------------#
# Moves GUI into a spread of the arcs to ask user to select             #
# which one to edit                                                     #
#-----------------------------------------------------------------------#
    sysdata.currentrender = "week"
    sysdata.currentmenu = "week_spread"
    drawSpread(sysdata.currentrender)
    return 0

def clickbtnWkd(event=0):
#-----------------------------------------------------------------------#
# Moves GUI into a spread of the arcs to ask user to select             #
# which one to edit                                                     #
#-----------------------------------------------------------------------#
    sysdata.currentrender = "wkd"
    sysdata.currentmenu = "wkd_spread"
    drawSpread(sysdata.currentrender)
    return 0

def clickbtnHome(event=0):
#-----------------------------------------------------------------------#
# Redraws the home screen                                               #
#-----------------------------------------------------------------------#
# NEED TO ADD TODAY / AWAY
    sysdata.currentrender = "week"
    sysdata.currentmenu = "home"
    drawHome()
    
def clickAMArc(event=0):
    sysdata.currentmenu = "am"
    updateEditLabels(sysdata.currentmenu)
    drawEdit(sysdata.currentmenu)
    
def clickPMArc(event=0):
    sysdata.currentmenu = "pm"
    updateEditLabels(sysdata.currentmenu)
    drawEdit(sysdata.currentmenu)
def clickbtnChangeTime(onoff, hourmin, updown):    
    if hourmin == "hour":
        updateTimings(onoff, 1 * updown)
    else:
        updateTimings(onoff, 0.25 * updown)
    updateEditLabels(sysdata.currentmenu)
    updateArcs()
def clearMidFrame():
##    btnAway.grid_forget()
##    btnSys.grid_forget()
##    btnWeek.grid_forget()
##    btnWkd.grid_forget()
##    btnHome.grid_forget()
    
    btnImgWeek.grid_forget()
    btnImgWkd.grid_forget()
    btnImgAway.grid_forget()
    btnImgSys.grid_forget()
    btnImgHome.grid_forget()

    lblOnHours.grid_forget()
    lblOnColon.grid_forget()
    lblOnMins.grid_forget()    
##    btnOnHourUp.grid_forget()
##    btnOnHourDown.grid_forget()
##    btnOnMinUp.grid_forget()
##    btnOnMinDown.grid_forget()
    btnImgOnHourUp.grid_forget()
    btnImgOnHourDown.grid_forget()
    btnImgOnMinUp.grid_forget()
    btnImgOnMinDown.grid_forget()
    
    lblOffHours.grid_forget()
    lblOffColon.grid_forget()
    lblOffMins.grid_forget() 
##    btnOffHourUp.grid_forget()
##    btnOffHourDown.grid_forget()
##    btnOffMinUp.grid_forget()
##    btnOffMinDown.grid_forget()
    btnImgOffHourUp.grid_forget()
    btnImgOffHourDown.grid_forget()
    btnImgOffMinUp.grid_forget()
    btnImgOffMinDown.grid_forget()
def drawSpread(render):
    updateArcs()
    clearMidFrame()
    
#    btnHome.grid(row=MidFrameRows, column=7, padx = Padding, sticky=N+E+S+W) 
    btnImgHome.grid(  row=MidFrameRows, column=0, padx = Padding, sticky=S+W, columnspan=2) 
        
    timingArcs.move("spread")
def drawHome():
    updateArcs()
    clearMidFrame()

##    btnAway.grid( row=0, column=0, padx = Padding, sticky=N+E+S+W)
##    btnSys.grid(  row=MidFrameRows, column=0, padx = Padding, sticky=N+E+S+W)
##    btnWeek.grid( row=0, column=7, padx = Padding, sticky=N+E+S+W)
##    btnWkd.grid(  row=MidFrameRows, column=7, padx = Padding, sticky=N+E+S+W)

    btnImgAway.grid( row=0, column=0, padx = Padding, sticky=N+W)
    btnImgSys.grid(  row=MidFrameRows, column=0, padx = Padding, sticky=S+W)
    btnImgWeek.grid( row=0, column=7, padx = Padding, sticky=N+E)
    btnImgWkd.grid(  row=MidFrameRows, column=7, padx = Padding, sticky=S+E)
    
    timingArcs.move("center")

def drawEdit(ampm):
#-----------------------------------------------------------------------#
# Draws the GUI with an arc on the right side and displays edit boxes   #
#-----------------------------------------------------------------------#
    updateArcs()
    clearMidFrame()

##    if ampm == "am" :
    onRow = 1
    offRow = MidFrameRows - 2
##    else:
##        onRow = MidFrameRows - 2
##        offRow = 1
        
    lblOnHours.grid(row=onRow, column=1-1, sticky=N+E+S+W, columnspan=2)
    lblOnColon.grid(row=onRow, column=3-1, sticky=N+E+S+W)
    lblOnMins.grid( row=onRow, column=4-1, sticky=N+E+S+W, columnspan=2)
    btnImgOnHourUp.grid(  row=onRow+1, column=1-1, sticky=N+E+S+W)
    btnImgOnHourDown.grid(row=onRow+1, column=2-1, sticky=N+E+S+W)
    btnImgOnMinUp.grid(   row=onRow+1, column=4-1, sticky=N+E+S+W)
    btnImgOnMinDown.grid( row=onRow+1, column=5-1, sticky=N+E+S+W)
    
    lblOffHours.grid(row=offRow, column=1-1, sticky=N+E+S+W, columnspan=2)
    lblOffColon.grid(row=offRow, column=3-1, sticky=N+E+S+W)
    lblOffMins.grid( row=offRow, column=4-1, sticky=N+E+S+W, columnspan=2)
    btnImgOffHourUp.grid(  row=offRow+1, column=1-1, sticky=N+E+S+W)
    btnImgOffHourDown.grid(row=offRow+1, column=2-1, sticky=N+E+S+W)
    btnImgOffMinUp.grid(   row=offRow+1, column=4-1, sticky=N+E+S+W)
    btnImgOffMinDown.grid( row=offRow+1, column=5-1, sticky=N+E+S+W)
    
#    btnHome.grid(row=MidFrameRows, column=0, sticky=N+E+S+W, columnspan=2)    
    btnImgHome.grid(row=MidFrameRows, column=0, padx = Padding, sticky=S+W, columnspan=2) 
       
    timingArcs.move("side", ampm)
    
def turnBoiler(onoff):
    if onoff == "on":
        sysdata.boiler = "on"
        lblStatus.config(text="Heating")
        lblStatus.config(fg=skin.colours.on)
    else:
        sysdata.boiler = "off"
        lblStatus.config(text="Idle")
        lblStatus.config(fg=skin.colours.off)
    
def checkHeating():
    timenow = int(time.strftime('%H')) + int(time.strftime('%M'))/60.0
    
    if sysdata.isaway == "away":
        cur_tim = sysdata.away
    elif (time.strftime('%A') == "Saturday") | (time.strftime('%A') == "Sunday"):
        cur_tim = sysdata.wkd
    else:
        cur_tim = sysdata.week

    if (cur_tim.amOn <= timenow) & (timenow < cur_tim.amOff):
        turnBoiler("On")
    elif (cur_tim.pmOn <= timenow) & (timenow < cur_tim.pmOff):
        turnBoiler("On")
    else:
        turnBoiler("Off")
        
def tick_1s():
    updateHeader()
    checkHeating()
    root.after(1000, tick_1s)
#-----------------------------------------------------------------------#
#                         MAIN CODE STARTS HERE                         #
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
# Initialise the GUI with it's Top, Middle & Bottom frames              #
# Top frame items are placed, Middle frame items are drawn later        #
#-----------------------------------------------------------------------#

sysdata = BoilerClasses.SysState() 
root = Tk()
skin = setupStyle()
small      = (skin.text.type, skin.text.sml)
smallBold  = (skin.text.type, skin.text.sml, "bold")
medium     = (skin.text.type, skin.text.med)
mediumBold = (skin.text.type, skin.text.med, "bold")
large      = (skin.text.type, skin.text.lrg)
largeBold  = (skin.text.type, skin.text.lrg, "bold")

# SETUP FRAMES
TopFrame = Frame(root, width=WinWidth, height = WinHeight*2/12)
MidFrame = Frame(root, width=WinWidth, height = WinHeight*9/12)
BotFrame = Frame(root, width=WinWidth, height = WinHeight*1/12)

TopFrame.grid_propagate(False)
MidFrame.grid_propagate(False)
BotFrame.grid_propagate(False)

TopFrame.grid(row=0, sticky=N+E+S+W)
MidFrame.grid(row=1, sticky=N+E+S+W)
BotFrame.grid(row=2, sticky=N+E+S+W)


# TOP FRAME LAYOUT
lblDay      = Label(TopFrame, font=(medium),    text="Day",  anchor=CENTER)
lblTimeHour = Label(TopFrame, font=(largeBold), text="XX",   anchor=E)
lblTimeCol  = Label(TopFrame, font=(largeBold), text=":",    anchor=CENTER)
lblTimeMin  = Label(TopFrame, font=(largeBold), text="XX",   anchor=W)
lblDate     = Label(TopFrame, font=(medium),    text="Date", anchor=CENTER)

##TopFrame.columnconfigure(0, weight=1)
##TopFrame.columnconfigure(1, weight=1)
##TopFrame.columnconfigure(2, weight=1)
##TopFrame.columnconfigure(3, weight=1)
##TopFrame.columnconfigure(4, weight=1)
##
##lblDay.grid(     row=0, column=0, sticky=N+E+S+W)
##lblTimeHour.grid(row=0, column=1, sticky=N+E+S+W)
##lblTimeCol.grid( row=0, column=2, sticky=N+E+S+W)
##lblTimeMin.grid( row=0, column=3, sticky=N+E+S+W)
##lblDate.grid(    row=0, column=4, sticky=N+E+S+W)

lblDay.place(     x=10,  y=15, anchor="w")
lblTimeHour.place(x=115, y=15, anchor="w")
lblTimeCol.place( x=151, y=15, anchor="w")
lblTimeMin.place( x=165, y=15, anchor="w")
lblDate.place(    x=210, y=15, anchor="w")

# MIDDLE FRAME LAYOUT - CIRCLE
timingArcs = BoilerClasses.TimeArc(MidFrame)

for i in range(0,8):
    MidFrame.columnconfigure(i, weight=1)
for j in range(0,MidFrameRows+1):
    MidFrame.rowconfigure(j, weight=1)

# NAVIGATION BUTTONS

imgWeek = PhotoImage(file = "week.png")
imgWkd  = PhotoImage(file = "wkd.png")
imgHome = PhotoImage(file = "home.png")
imgSys  = PhotoImage(file = "gears.png")
imgBack = PhotoImage(file = "back.png")
imgAway = PhotoImage(file = "back.png")
imgUp   = PhotoImage(file = "up.png")
imgDown = PhotoImage(file = "down.png")

imgWeek = imgWeek.subsample(10, 10)
imgWkd  = imgWkd.subsample( 10, 10)
imgHome = imgHome.subsample(10, 10)
imgSys  = imgSys.subsample( 10, 10)
imgBack = imgBack.subsample(10, 10)
imgAway = imgAway.subsample(10, 10)
imgUp   = imgUp.subsample(  20, 20)
imgDown = imgDown.subsample(20, 20)

##btnAway = Button(MidFrame, text="Away", command = clickbtnAway)
##btnSys  = Button(MidFrame, text="Sys",  command = clickbtnSys)
##btnWeek = Button(MidFrame, text="Week", command = clickbtnWeek)
##btnWkd  = Button(MidFrame, text="Wkd",  command = clickbtnWkd)
##btnHome = Button(MidFrame, text="Home", command = clickbtnHome)

btnImgWeek = Label(MidFrame, image = imgWeek)
btnImgWkd  = Label(MidFrame, image = imgWkd)
btnImgAway = Label(MidFrame, image = imgAway)
btnImgSys  = Label(MidFrame, image = imgSys)
btnImgHome = Label(MidFrame, image = imgHome)

btnImgWeek.bind("<Button-1>", clickbtnWeek)
btnImgWkd.bind( "<Button-1>", clickbtnWkd)
btnImgAway.bind("<Button-1>", clickbtnAway)
btnImgSys.bind( "<Button-1>", clickbtnSys)
btnImgHome.bind("<Button-1>", clickbtnHome)

topleft = (Padding, 0, Padding + buttonWidth, Padding + buttonHeight)

# EDIT TIMINGS
lblOnHours  = Label(MidFrame, font=(largeBold), text="x")
lblOnColon  = Label(MidFrame, font=(largeBold), text=":")
lblOnMins   = Label(MidFrame, font=(largeBold), text="x")
##btnOnHourUp    = Button(MidFrame, text="^", command = lambda i="on", j="hour",k= 1 :clickbtnChangeTime(i,j,k))
##btnOnHourDown  = Button(MidFrame, text="v", command = lambda i="on", j="hour",k=-1 :clickbtnChangeTime(i,j,k))
##btnOnMinUp     = Button(MidFrame, text="^", command = lambda i="on", j="min", k= 1 :clickbtnChangeTime(i,j,k))
##btnOnMinDown   = Button(MidFrame, text="v", command = lambda i="on", j="min", k=-1 :clickbtnChangeTime(i,j,k))
btnImgOnHourUp    = Label(MidFrame, image = imgUp)
btnImgOnHourDown  = Label(MidFrame, image = imgDown)
btnImgOnMinUp     = Label(MidFrame, image = imgUp) 
btnImgOnMinDown   = Label(MidFrame, image = imgDown) 
btnImgOnHourUp.bind(  "<Button-1>",  lambda i="on", j="hour",k= 1 :clickbtnChangeTime(i,j,k))
btnImgOnHourDown.bind("<Button-1>",  lambda i="on", j="hour",k=-1 :clickbtnChangeTime(i,j,k))
btnImgOnMinUp.bind(   "<Button-1>",  lambda i="on", j="min", k= 1 :clickbtnChangeTime(i,j,k))
btnImgOnMinDown.bind( "<Button-1>",  lambda i="on", j="min", k=-1 :clickbtnChangeTime(i,j,k))

lblOffHours = Label(MidFrame, font=(largeBold), text="x")
lblOffColon = Label(MidFrame, font=(largeBold), text=":")
lblOffMins  = Label(MidFrame, font=(largeBold), text="x")
##btnOffHourUp   = Button(MidFrame, text="^", command = lambda i="off", j="hour",k= 1 :clickbtnChangeTime(i,j,k))
##btnOffHourDown = Button(MidFrame, text="v", command = lambda i="off", j="hour",k=-1 :clickbtnChangeTime(i,j,k))
##btnOffMinUp    = Button(MidFrame, text="^", command = lambda i="off", j="min" ,k= 1 :clickbtnChangeTime(i,j,k))
##btnOffMinDown  = Button(MidFrame, text="v", command = lambda i="off", j="min" ,k=-1 :clickbtnChangeTime(i,j,k))
btnImgOffHourUp    = Label(MidFrame, image = imgUp)
btnImgOffHourDown  = Label(MidFrame, image = imgDown)
btnImgOffMinUp     = Label(MidFrame, image = imgUp) 
btnImgOffMinDown   = Label(MidFrame, image = imgDown) 
btnImgOffHourUp.bind(  "<Button-1>",  lambda i="off", j="hour",k= 1 :clickbtnChangeTime(i,j,k))
btnImgOffHourDown.bind("<Button-1>",  lambda i="off", j="hour",k=-1 :clickbtnChangeTime(i,j,k))
btnImgOffMinUp.bind(   "<Button-1>",  lambda i="off", j="min" ,k= 1 :clickbtnChangeTime(i,j,k))
btnImgOffMinDown.bind( "<Button-1>",  lambda i="off", j="min" ,k=-1 :clickbtnChangeTime(i,j,k))

timingArcs.grid(row=0, column=0, rowspan=8, columnspan=8, sticky=N+E+S+W)

timingArcs.tag_bind(timingArcs.amOn,  "<Button-1>", clickAMArc)
timingArcs.tag_bind(timingArcs.amOff, "<Button-1>", clickAMArc)
timingArcs.tag_bind(timingArcs.pmOn,  "<Button-1>", clickPMArc)
timingArcs.tag_bind(timingArcs.pmOff, "<Button-1>", clickPMArc)

# BOTTOM FRAME LAYOUT
lblStat   = Label(BotFrame,font=(small),     text=" Status:", anchor=CENTER)
lblStatus = Label(BotFrame,font=(smallBold), text="STATUS",   anchor=CENTER)
lblStat.config(  fg=skin.colours.off)
lblStatus.config(fg=skin.colours.off)

lblStat.grid(  row=0, column=0, sticky=E+S+W)
lblStatus.grid(row=0, column=1, sticky=E+S+W)

#-----------------------------------------------------------------------#
# Populate data and begin GUI mainloop                                  #
#-----------------------------------------------------------------------#

sysdata.currentrender = "week"
sysdata.currentmenu = "home"
drawHome()
updateArcs()
tick_1s()
root.mainloop()